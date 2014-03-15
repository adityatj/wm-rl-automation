import mechanize
import cookielib
import re
import urllib, zipfile, StringIO, urllib2, argparse
import os
import sys

__author__ = 'TJ Aditya'
__version__ = '1.5'

#Print Banner
print '|--------------------------------------------------|'
print '| * Retail-Link Automation Tool by adityatj(GIT) * |'
print '|--------------------------------------------------|'
print '\n\n'

#Globals
mark = '[*]'

#Parse the script arrays
def parseStr(s):
    s = re.sub("\"", "", s)
    s = re.sub(" ", "", s)
    tmp = s.split('=')
    return tmp[1]

#ArgParse stuff
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--miss", help="Missing files text")
parser.add_argument("-c", "--cc", help="Country code")
parser.add_argument("-s", "--scc", help="Sub-Country code", type=int)
parser.add_argument("-d", "--retrieve", help="Retrieve mode", action="store_true")
parser.add_argument("-r", "--run", help="Re-run mode", action="store_true")

#Parsing args
args = parser.parse_args()
miss_file_name = args.miss
country_code = args.cc
sub_cc = args.scc

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

####################
#* Retrieve files *#
####################

if args.retrieve:
    #Open login url
    br.open('https://rllogin.wal-mart.com/rl_security/rl_logon.aspx?ServerType=IIS1&redir=%2F')
    print mark + 'Connection established'

    #Get the form
    br.select_form(nr=0)
    print mark + 'Logging in...'

    #Get the User and Pass (very bad system, needs to optimized)
    fp = open('pass.txt', 'r')
    user = passwd = ''
    for line in fp:
        pass_dir = line.split(':')
        if pass_dir[0] == country_code:
            #create folder
            if not os.path.exists(pass_dir[0] + "/"):
                os.makedirs(pass_dir[0])
            user = pass_dir[1]
            passwd = pass_dir[2]

            #Set the uname and pass
            br.form['txtUser'] = user.strip()
            br.form['txtPass'] = passwd.strip()

            #Submit
            br.submit()

            #Open stats link
            br.open('https://retaillink.wal-mart.com/mydss/status_get_data.aspx?ApplicationId=300&bPortlet=False')

            #Get the file attribs javascript line
            print mark + 'Getting files stats and attribs...'
            obj = br.response()
            dummy = obj.readline()
            while not 'PopulateClientSide()' in dummy:
                dummy = obj.readline()

            #Process the script
            print mark + 'Processing stats...'
            arr = dummy.split(';')
            arr_length = len(arr)
            arr[1] = re.sub(r'.*window', 'window', arr[1])

            #Open missing files list
            print mark + 'Retrieving files...'
            fp = open('miss.txt', 'r')
            reqs = fp.readlines()
            reql = len(reqs)
            for i in range(len(reqs)):
                #print mark + 'Retrieving ' + req_name + '.zip'
                req_name = reqs[i].strip()
                counter = 0
                q_id = app_id = job_id = status = ext= file_name = ''
                while counter < arr_length:
                    if req_name in arr[counter]:
                        q_id = parseStr(arr[counter-3])
                        app_id=parseStr(arr[counter-5])
                        ext=parseStr(arr[counter-6])
                        file_name=parseStr(arr[counter-7])
                        job_id=parseStr(arr[counter-9])
                        status=parseStr(arr[counter-10])
                        counter=arr_length
                    counter = counter + 1
                if status == 'D' or status == 'R':
                    print mark + 'Retrieving: ' + req_name + '.' + ext + '...'
                    site = 'https://retaillink.wal-mart.com' +file_name + '.' + ext
                    #d_url = 'Status_retrieve_request.aspx?questionid=' + q_id + '&applicationid=' + app_id + '&JobId=' + job_id + '&status=' + status + '&Extension=' + ext + '&filename=' + file_name + '&reqname=' + req_name
                    #print site
                    br.open(site)
                    obj = br.response()
                    f = open(pass_dir[0] + "/" + req_name + '.' + ext, 'wb')
                    f.write(obj.read())
                    f.flush()
                    f.close()
                    print mark + req_name + '.' + ext + ' Done!'

