import urllib
import urllib2
import os.path
import json

__author__ = 'TJ Aditya'
__version__ = '0.2'

#Strings
bullet = '[*]'
blank_bullet = '   '
gem_detail_url = 'https://retaillink.wal-mart.com/edi/gem/Batch/GetBatchDetail'
gem_count_url = 'https://retaillink.wal-mart.com/edi/gem/Batch/GetBatchDetailCount'
gem_ret_url = 'https://retaillink.wal-mart.com/edi/gem/Batch/SaveStatus'
base_url = 'https://rllogin.wal-mart.com/rl_security/rl_logon.aspx?ServerType=IIS1&CTAuthMode=BASIC&language=en&CT_ORIG_URL=%2Fhome%2F&ct_orig_uri=%2Fhome%2F'


#Setting up the Cookie Jar#
#################################################

COOKIEFILE = 'cookies.lwp'
# the path and filename to save your cookies in

cj = None
ClientCookie = None
cookielib = None

# Let's see if cookielib is available
try:
    import cookielib
except ImportError:
    # If importing cookielib fails
    # let's try ClientCookie
    try:
        import ClientCookie
    except ImportError:
        # ClientCookie isn't available either
        urlopen = urllib2.urlopen
        Request = urllib2.Request
    else:
        # imported ClientCookie
        urlopen = ClientCookie.urlopen
        Request = ClientCookie.Request
        cj = ClientCookie.LWPCookieJar()

else:
    # importing cookielib worked
    urlopen = urllib2.urlopen
    Request = urllib2.Request
    cj = cookielib.LWPCookieJar()
    # This is a subclass of FileCookieJar
    # that has useful load and save methods

if cj is not None:
# we successfully imported
# one of the two cookie handling modules

    if os.path.isfile(COOKIEFILE):
        # if we have a cookie file already saved
        # then load the cookies into the Cookie Jar
        cj.load(COOKIEFILE)

    # Now we need to get our Cookie Jar
    # installed in the opener;
    # for fetching URLs
    if cookielib is not None:
        # if we use cookielib
        # then we get the HTTPCookieProcessor
        # and install the opener in urllib2
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

    else:
        # if we use ClientCookie
        # then we get the HTTPCookieProcessor
        # and install the opener in ClientCookie
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
        ClientCookie.install_opener(opener)
#################################################
#RL Login

p = {}
p['__EVENTTARGET'] = ''
p['__EVENTARGUMENT'] = ''
p['__VIEWSTATE'] = '/wEPDwUJMzA0NTk5Njc2D2QWAmYPZBYCAgkPZBYCZg9kFgJmD2QWAgIBD2QWBAIBD2QWAmYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgICBQ9kFgICAg9kFgJmDw8WAh4HVmlzaWJsZWhkFgICAQ8PFgIfAGhkZAICD2QWAmYPZBYCAgEPD2QWBB4Lb25tb3VzZW92ZXIFG3RoaXMuY2xhc3NOYW1lPSdidG4gYnRuaG92Jx4Kb25tb3VzZW91dAUUdGhpcy5jbGFzc05hbWU9J2J0bidkZKQk1bS9ScH2nbzBevimAtOgDmR4'
p['__EVENTVALIDATION'] = '/wEWBwKLhvbwAwK145qeCgK7iKX4CAKgmu7gDwLB2tiHDgLKw6LdBQLvz/GACsoX4ysI6TvqtSSds6M5aOR3HaHH'
p['hidFailedLoginCount'] = ''
p['redirect'] = '/home/'
p['hidPwdErrHandledFlag'] = 'FALSE'
p['txtUser'] = '<Your GEM Mailbox username>'
p['txtPass'] = '<Your GEM Mailbox password>'
p['Login'] = 'Logon'

data = urllib.urlencode(p)

head = {}
head['Accept'] = 'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*'
head['Referer'] = 'https://rllogin.wal-mart.com/rl_security/rl_logon.aspx?ServerType=IIS1&CTAuthMode=BASIC&language=en&CT_ORIG_URL=%2Fhome%2F&ct_orig_uri=%2Fhome%2F'
head['Accept-Language'] = 'en-US'
head['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; Zune 4.7)'
head['Content-Type'] = 'application/x-www-form-urlencoded'
head['Accept-Encoding'] = 'gzip, deflate'
head['Host'] = 'rllogin.wal-mart.com'
head['Content-Length'] = len(data)
head['Connection'] = 'Keep-Alive'
head['Cache-Control'] = 'no-cache'

req = Request(base_url, data, head)
res = urlopen(req)
print bullet + 'Logged into Retail-Link'

print bullet + 'Submitting Batches...'
f = open('accounts.txt', 'r')
for line in f:
    account = line.strip()
    print bullet + 'Account: ' + account


    #Getting Batch Count from GEM for the respective account

    cp = {}
    cp['Batch'] = 'bid'
    cp['BatchValue'] = '*' + account + '*'
    cp['matchFlag'] = ''
    cp['notmatchFlag'] = ''
    cp['FromDate'] = ''
    cp['ToDate'] = ''
    cp['Count'] = '0'
    cp['FromTime'] = ''
    cp['ToTime'] = ''
    cp['FromNumDays'] = ''
    cp['FromNumTime'] = ''
    cp['ToNumDays'] = ''
    cp['ToNumTime'] = ''
    cp['MailboxId'] = 'PMWXTtXG'
    cp['LoggedInUserId'] = '<Your GEM Mailbox username>'
    cp['BrowseList'] = '-1'
    cp['ReflagList'] = '-1'
    cp['listcmd'] = 'PMWXTtXG|*' + account + '*|||||'
    cp['pageIndex'] = '0'

    cpd = urllib.urlencode(cp)

    hc = {}
    hc['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    hc['Accept-Language'] = 'en-us'
    hc['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; Zune 4.7)'
    hc['Content-Type'] = 'application/x-www-form-urlencoded'
    hc['Accept-Encoding'] = 'gzip, deflate'
    hc['Host'] = 'retaillink.wal-mart.com'
    hc['Content-Length'] = len(cpd)
    hc['Connection'] = 'Keep-Alive'
    hc['Cache-Control'] = 'no-cache'
    hc['x-requested-with'] = 'XMLHttpRequest'

    reqc = Request(gem_count_url, cpd, hc)
    resc = urlopen(reqc)
    batch_count = 0
    for line in resc:
        batch_count = int(line)
    print blank_bullet + 'Batch Count: %d' % (batch_count)
    if batch_count > 0:
        #Getting Batch Details for the account

        dp = {}
        dp['Batch'] = 'bid'
        dp['BatchValue'] = '*' + account + '*'
        dp['matchFlag'] = ''
        dp['notmatchFlag'] = ''
        dp['FromDate'] = ''
        dp['ToDate'] = ''
        dp['Count'] = batch_count
        dp['FromTime'] = ''
        dp['ToTime'] = ''
        dp['FromNumDays'] = ''
        dp['FromNumTime'] = ''
        dp['ToNumDays'] = ''
        dp['ToNumTime'] = ''
        dp['MailboxId'] = 'PMWXTtXG'
        dp['LoggedInUserId'] = '<Your GEM Mailbox username>'
        dp['BrowseList'] = '-1'
        dp['ReflagList'] = '-1'
        dp['listcmd'] = 'PMWXTtXG|*' + account + '*|||||'
        dp['pageIndex'] = '0'
        dp['_search'] = 'false'
        dp['nd'] = '1386524543451'
        dp['rows'] = batch_count
        dp['page'] = '1'
        dp['sidx'] = 'MailboxGroupBy asc, BatchNumber'
        dp['sord'] = 'asc'

        dpd = urllib.urlencode(dp)

        hd = {}
        hd['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        hd['Accept-Language'] = 'en-us'
        hd['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; Zune 4.7)'
        hd['Content-Type'] = 'application/x-www-form-urlencoded'
        hd['Accept-Encoding'] = 'gzip, deflate'
        hd['Host'] = 'retaillink.wal-mart.com'
        hd['Content-Length'] = len(dpd)
        hd['Connection'] = 'Keep-Alive'
        hd['Cache-Control'] = 'no-cache'
        hd['x-requested-with'] = 'XMLHttpRequest'

        reqd = Request(gem_detail_url, dpd, hd)
        resd = urlopen(reqd)

        json_data = resd.readline()
        pdata = json.loads(json_data)

        for row in pdata['rows']:
            batch_id = row['cell'][0]
            status = row['cell'][5].split(':')[1]
            if status == 'System Re-Queue':
                #Re-Transmit the Batch ID
                print blank_bullet + 'Batch ID: ' + batch_id
                print blank_bullet + 'Current Status: ' + status
                rp = {}
                rp['batchnr'] = batch_id
                rp['status'] = 30

                rpd = urllib.urlencode(rp)

                hr = {}
                hr['Accept'] = 'application/json, text/javascript, */*; q=0.01'
                hr['Accept-Language'] = 'en-us'
                hr['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; Zune 4.7)'
                hr['Content-Type'] = 'application/x-www-form-urlencoded'
                hr['Accept-Encoding'] = 'gzip, deflate'
                hr['Host'] = 'retaillink.wal-mart.com'
                hr['Content-Length'] = len(rpd)
                hr['Connection'] = 'Keep-Alive'
                hr['Cache-Control'] = 'no-cache'
                hr['x-requested-with'] = 'XMLHttpRequest'

                reqr = Request(gem_ret_url, rpd, hr)
                resr = urlopen(reqr)

                val = resr.readline()
                if val == 'true':
                    print bullet + 'Re-Transmission Status: Re-Transmitted Successfully'
                else:
                    print bullet + 'Re-Transmission Status: Re-Transmission Failed'


