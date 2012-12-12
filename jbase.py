from subprocess import Popen, PIPE
import os
import sys
import jError

_AM=chr(254);   _VM=chr(253);   _SVM=chr(252);   _ERROR='!#%'
INHERIT_PARENT_AFFINITY = 0x00010000

def setJbaseEnv():
    os.environ['JBCBACKGROUND'] = '1'
    os.environ['JBCFLUSH_STDOUT'] = '1'
    os.environ['path'] += ';%JBCRELEASEDIR%\\bin;c:\\ourjapps\mc30\\bin;c:\\ourjapps\\ob\\bin;c:\\ourjapps\\dm\\bin;c:\\ourjapps\\blat'
    os.environ['JBCOBJECTLIST'] = 'c:\\ourjapps\\mc30\\lib;c:\\ourjapps\\ob\\lib;c:\\ourjapps\\dm\\lib'
    os.environ['JEDIFILEPATH'] = 'c:\\ourjdata\\th.data;c:\\ourjdata\\shared.data;c:\\ourjapps\\mc30;c:\\ourjapps\\ob;c:\\ourjapps\\dm;c:\\ourjdata\\th.data\\work'
    os.environ['JEDIFILENAME_MD'] = 'c:\\ourjapps\\mc30\\md]d'
        
class jbase:
 
    def __init__ (self):
#        try:
#            savestdout = stdout;  stdout = None
#            os.system("taskkill /im JSLAVE.exe /f")
#            stdout = savestdout
#        except: pass
        
        setJbaseEnv()
        try:
            self.proc = Popen('JSLAVE.exe', bufsize=0, shell=False, stdout=PIPE, stdin=PIPE, creationflags=0)
        except: raise
        # !!! the above process will not be killed unless specifically commanded to and will use all CPU
        # !!! when it is orphaned
#        pid = self.proc.pid

    def _submit (self, *args): 
        command = ''
        for arg in args:
            command += _AM + arg
                       
        self.proc.stdin.write((command[1:]).replace('\n', '') + '\n')
        return self.proc.stdout.readline()[:-2] # !!! this will hang if buffer is empty!!!!
           
    def read (self, filenm, itemid):  
        try:         
            rec = self._submit('READ', filenm, itemid)
            if rec[0:3] == _ERROR:
                raise jError('no such file')
            else:
                return rec.split(_AM)
        except:
            return ''

    def oconv (self, indata, cnv): 
        oval = self._submit('OCONV', indata, cnv)
        if oval[0:3] == _ERROR:
            raise jError('illegal oconv')
        else:
            return oval

    def query (self, qry):
        qry = qry.upper()
        words = qry.split(' ')
        fname = words[1]
        lst = self._submit('SELECT', 'QUERY', '', words[1], qry)
        return lst.split(_AM)
    
    def off (self):
        return self._submit('OFF')

def writeImmeadiatelyToPopen(openCmd, textToWrite):
    openCmd.write(textToWrite.encode())
    openCmd.flush()
    
if __name__ == '__main__': 
    print 'main ' 
    jbs = jbase()
    
    lst = jbs.query('SSELECT NOTETYPE WITH 3 = "G"')
    print lst
    print jbs.read('RJCD', '126')
    print jbs.oconv('13456', 'mr2')
    
    allrec = jbs.read('MC.USER', 'everyone')
    print 'ar: ' + str(allrec)

#    stdout = proc.communicate('HELLO!\n\r')
    jbs.proc.terminate()
