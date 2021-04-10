from datetime import datetime

class VaccineDay:
    
    def __init__(self, index, dosing_date, total):
        self.index = index
        self.dosing_date = dosing_date
        '''
        datetime ( 
        year=int((dosing_date )[0:4]), 
        month=int((dosing_date )[5:7]), 
        day=int((dosing_date )[8:10]) )
        hour = 0, 
        minute = 0, 
        second = 0 )
        '''
        self.total = total