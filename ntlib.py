# in /jimpy  filename: pickmod.py
from subprocess import Popen, PIPE
from smtplib import SMTP
import os
import datetime
import time
import sys
import random

def setSyspath ():
    machine = os.getenv('COMPUTERNAME', 'unknown')
    if machine == '3HAB-DB01':  # location of data files on 3Hab server
        baselib = '\\ourjapps\\mcpy\\eclipse_wksp\\jimpy'
        graphlib = 'c:\\ourjapps\\mcpy\\eclipse_wksp\\ChartDirector\\lib'
    else:
        baselib = '\\users\\jdp\\documents\\eclipse_wksp\\jimpy'
        graphlib = 'c:\\users\\jdp\\documents\\eclipse_wksp\\ChartDirector\\lib'
    sys.path.append(baselib)
    sys.path.append(graphlib)
                    
def deliverHtml (doc):
    hdr = """HTTP/1.0 200 OK
    Date: Fri, 31 Dec 1999 23:59:59 GMT
    Content-Type: text/html
    Content-Length: """
    hdr += str(len(doc))
    print hdr
    print
    print doc
    
def readURL(url):
    import urllib2

#    url = 'http://wwiz.ipcmailwell.com/webwiz/wwiz.exe/wwiz.asp?wwizmstr=PY.READ&file=' + fileName + '&item=' + itemId
    response = urllib2.urlopen (url)
    doc = response.read()

    rec = doc.splitlines()
    rec[0] = rec[0][6:] 
    
#    for i, fld in enumerate(rec):
#            rec[i] = fld.split(']')
    return rec
 
def exec_command(cmd_args):
    """
    Quick wrapper around subprocess to exec shell command and pass back 
    stdout, stderr, and the return code..
     Required Arguments: 
        cmd_args
            The args to pass to subprocess.  
    Usage:
    .. code-block:: python
        (stdout, stderr, retcode) = exec_command(['ls', '-lah']) 
    """
    proc = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = proc.communicate()
    proc.wait()
 
    return (stdout, stderr, proc.returncode)


def catch(func, dflt, *args, **kwargs):
    try: return func(*args, **kwargs)
    except: return dflt
    
# x = catch(lambda e : ls[e], 'not there', n)
# x = catch(int, '0', '132.abc')

def lget(lst, pos, dflt=""):
    try: return lst[pos]
    except: return dflt

def sendEmail(toAddr, subject, msg, ccs=[], bccs=[], attachements=[]):
    HOST = "mx1.hosting.zimcom.net"
    PORT = 25
    ACCOUNT = "jimpaul@3hab.com" # put your gmail email account here
    PASSWORD = "37793779" # put your gmail email password here
    FROMADDR = 'python@3hab.com'
    server = SMTP(HOST,PORT)
    server.set_debuglevel(1) # you don't need this (comment out to avoid debug messages)
#sendEmail( ['jimpaul@3hab.com'], 'this is just a test999', "hello ccs!" )
#    server.ehlo()
#    server.starttls()
#    server.ehlo()
    server.login(ACCOUNT, PASSWORD)
    message = "From: %s\r\n" % FROMADDR\
    + "To: %s\r\n" % toAddr\
    + "CC: %s\r\n" % ",".join(ccs)\
    + "Subject: %s\r\n" % subject\
    + "\r\n"\
    + msg
    toAddrs = [toAddr] + ccs + bccs
    server.sendmail(FROMADDR, toAddrs, message)
    server.quit()

def strToDate(datestr):
    datestr = datestr.replace('.', ' ').replace('-', ' ').replace('/', ' ').replace(',', ' ').replace('\\', ' ')
    datelst = datestr.split(' ')
    try: 
        year = lget(datelst, 2)
        if year == '':
            t = datetime.date.today()
            year = t.strftime('%Y')
        if len(year) == 2: year = '20' + year
        return datetime.date(int(year), int(datelst[0]), int(datelst[1]))
#time.strptime(datestr, "%d %m %Y") should work too but it produces a tupple not a time
    except: 
        return None

def dateToStr (dt):  
    try: return dt.strftime('%m-%d-%y') 
    except: return ''
    
def printErr(*args):
    holdErr = sys.stderr
    sys.stderr = open('c:\debug.txt', 'a')
    sys.stderr.write(' '.join(map(str,args)) + '\n')
    sys.stderr = holdErr
     
def whereis(program):
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and \
           not os.path.isdir(os.path.join(path, program)):
            return os.path.join(path, program)
    return None

def randomName():
    """You msut have dummy_names.txt in your CWD folder.
    returns firstName & lastName, both mixed case.  At " Inc." or " Co. "to the one of the names
    to get psuedo companies """
    fname = os.path.join(os.path.dirname(os.path.realpath(__file__ )), "dummy_names.txt")
    mmList = [line.strip().replace(' ','') for line in open(fname, 'r')]
    pair = mmList[random.randint(0, len(mmList)-1)].split(',')
    lname = pair[0][:1].upper() + pair[0][1:].lower()
    fname = pair[1][:1].upper() + pair[1][1:].lower()
    return fname, lname
                  
def fileReplace (myPath, oldText, newText):
    from os import walk

    for (dirpath, dirname, filenames) in os.walk(myPath):
        break
    
    for fil in filenames:
        fullfil = os.path.join(dirpath, fil)
        print fullfil
        rec = open(fullfil, 'r').read()
        rec = rec.replace(oldText, newText)
        open(fullfil, 'w').write(rec)

def fileSearch (myPath, findText, walkdown=True):
    """ print out all occurance of findText in a folder
    w or w/o recursion
    """
    flst = getFiles(myPath, walkdown)
    for fil in flst:
        fOpen = open(fil, 'r')
        rec = fOpen.readlines()
        l=0
        for ln in rec:
            l += 1
            pos = ln.find(findText)
            #print str(pos) + ' ' + ln
            if pos > 0:
                print fil + '   ln: ' + str(l)
                print '   ' + ln.lstrip()

def getFiles (path, walkdown=True, filelist=[]):
    """ returns a list of all files in a folder, w/wo recursion"""
    for (dirpath, dirname, filenames) in os.walk(path):
        break
    
    if walkdown:
        for dir in dirname:
            fullpath = os.path.join(dirpath, dir)
            for (dpath, dnm, fnames) in os.walk(fullpath):
                break
    
            for fn in fnames:
                fullfn = os.path.join(dpath, fn)
                filelist.append(fullfn)
            getFiles(fullpath, walkdown, filelist)
        return filelist
    else:
        return [os.path.join(dirpath, f) for f in filenames]
    
if __name__ == '__main__': 
    print 'main '
    x = raw_input('ff: ')
    if x != 'f': exit()
    fileSearch('C:\\apython', 'setlocal', True)

        
#    sendEmail( ['jimpaul@3hab.com'], 'this is just a test999', "hello ccs!" )
#    for filename in os.listdir("."):
#        print  filename
#    for f in nested('.'):
#        print f
