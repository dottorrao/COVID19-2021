import os.path
import datetime

class LogManager:

    def __init__(self, logPathFile, logFileName, levelLog):
        self.logPathFile = logPathFile
        self.fileName = logFileName
        self.levelLog = levelLog
       
    def write(self, message, suppressconsole):
        if not (suppressconsole):
            print( message )
        f = open( str(self.logPathFile) + "/" + str(self.fileName), "a" )
        f.write(message + "\n")
        f.close()

    def writeWithTimestemp(self, message, suppressconsole):
        now = datetime.datetime.now()
        if not (suppressconsole):
            print( str(now) + " : " + message )
        f = open( str(self.logPathFile) + "/" + str(self.fileName), "a" )
        f.write( str(now) + " : " + message + "\n" )
        f.close()