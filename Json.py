import urllib.request, json 
from Log import LogManager
import pathlib
import ssl

class JsonRead:

    def __init__(self, url):
        
        logManager = LogManager (pathlib.Path().absolute(),"Covid19-2021.log","debug")
        logManager.writeWithTimestemp ("====================================")
        logManager.writeWithTimestemp ("=  JsonRead inizializazion module  =")
        logManager.writeWithTimestemp ("====================================")
        
        self.url = url
    
    def getData (self):
        logManager = LogManager (pathlib.Path().absolute(),"Covid19-2021.log","debug")
        logManager.writeWithTimestemp ("JsonRead.py: Getting Json data from " + self.url)
        
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            with urllib.request.urlopen(self.url) as url:
                data = json.loads(url.read().decode())
            return data

        except Exception as e:
            logManager.writeWithTimestemp ("JsonRead.py: !! Error on getting json data... !!")
            logManager.writeWithTimestemp (str(e))
    
    def getDataWithFilter (self,filter,value):
        logManager = LogManager (pathlib.Path().absolute(),"Covid19-2021.log","debug")
        logManager.writeWithTimestemp ("JsonRead.py: Getting Json data from " + self.url)
        
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            with urllib.request.urlopen(self.url) as url:
                data = json.loads(url.read().decode())
                data = [x for x in data["data"] if x[filter] == value]
            return data

        except Exception as e:
            logManager.writeWithTimestemp ("JsonRead.py: !! Error on getting json data... !!")
            logManager.writeWithTimestemp (str(e))