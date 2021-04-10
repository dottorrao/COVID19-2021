import urllib.request, json 
from Log import LogManager
import pathlib
import ssl

class JsonRead:

    def __init__(self, url):
        
        logManager = LogManager (pathlib.Path().absolute(),"Covid19-2021.log","debug")
        logManager.writeWithTimestemp ("====================================",True)
        logManager.writeWithTimestemp ("=  JsonRead inizializazion module  =",True)
        logManager.writeWithTimestemp ("====================================",True)
        
        self.url = url
    
    def getData (self):
        logManager = LogManager (pathlib.Path().absolute(),"Covid19-2021.log","debug")
        logManager.writeWithTimestemp ("JsonRead.py - getData: Getting Json data from " + self.url,True)
        
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            with urllib.request.urlopen(self.url) as url:
                data = json.loads(url.read().decode())
            return data

        except Exception as e:
            logManager.writeWithTimestemp ("JsonRead.py - getData: !! Error on getting json data... !!",True)
            logManager.writeWithTimestemp (str(e),True)
    
    def getDataWithFilter (self,filter,value):
        logManager = LogManager (pathlib.Path().absolute(),"Covid19-2021.log","debug")
        logManager.writeWithTimestemp ("JsonRead.py - getDataWithFilter : Getting Json data from " + self.url,True)
        
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            with urllib.request.urlopen(self.url) as url:
                data = json.loads(url.read().decode())
                data = [x for x in data["data"] if x[filter] == value]
            return data

        except Exception as e:
            logManager.writeWithTimestemp ("JsonRead.py - getDataWithFilter ERROR: !! Error on getting json data... !!",True)
            logManager.writeWithTimestemp (str(e),True)
    
    def getDataWithFilterPROV (self,filter,value):
        logManager = LogManager (pathlib.Path().absolute(),"Covid19-2021.log","debug")
        logManager.writeWithTimestemp ("JsonRead.py - getDataWithFilterPROV : Getting Json data from " + self.url,True)
        
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            with urllib.request.urlopen(self.url) as url:
                data = json.loads(url.read().decode())
                data = [x for x in data if x[filter] == value]
            return data

        except Exception as e:
            logManager.writeWithTimestemp ("JsonRead.py - getDataWithFilter ERROR: !! Error on getting json data... !!",True)
            logManager.writeWithTimestemp (str(e),True)