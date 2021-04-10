from Json import JsonRead
from Log import LogManager
import pathlib
from VaccineSummary import VaccineSummary
from VaccineDay import VaccineDay
from Covid19DataSet import Covid19DataSet
from Covid19DataSetProv import Covid19DataSetProv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from Update import Update
import configparser 
import locale

import numpy as np
import mplcursors

suppressConsole = True

locale.setlocale(locale.LC_ALL, 'en_US')

logManager = LogManager (pathlib.Path().absolute(),"Covid19-2021.log","debug" )
logManager.writeWithTimestemp ("=============================",suppressConsole )
logManager.writeWithTimestemp ("=  CalculateResults module  =",suppressConsole )
logManager.writeWithTimestemp ("=============================",suppressConsole )

configParser = configparser.RawConfigParser()   
configFilePath = r'./config.ini'
configParser.read(configFilePath)

intervalDay = int ( configParser.get('settings', 'dayInterval') )
minor_locator_interval = int ( configParser.get('settings', 'minor_locator_interval') )
max_locator_interval = int ( configParser.get('settings', 'max_locator_interval') )
imageOutputPath = configParser.get('settings', 'images_output_path')

#########################################################################################
# Processing data from 'anagrafica-vaccini-summary-latest.json' file with defined mapping
#########################################################################################

#getting last update timestamp
jr = JsonRead("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/last-update-dataset.json")
jsonD = jr.getData()
up = Update (jsonD["ultimo_aggiornamento"])

arrayVaccineSummary = []
try:
    logManager.writeWithTimestemp ("CalculateResults.py: Getting 'Vaccine Summary' data...",suppressConsole )
    jr = JsonRead("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.json")
    jsonD = jr.getData()
    logManager.writeWithTimestemp ("CalculateResults.py: 'Vaccine Summary' data fetched! Processing...",suppressConsole )
    for i in range( len(jsonD["data"]) ):
        vs = VaccineSummary(    jsonD["data"][i]["index"], 
                                jsonD["data"][i]["fascia_anagrafica"],
                                jsonD["data"][i]["totale"],
                                jsonD["data"][i]["sesso_maschile"],
                                jsonD["data"][i]["sesso_femminile"],
                                jsonD["data"][i]["categoria_operatori_sanitari_sociosanitari"],
                                jsonD["data"][i]["categoria_personale_non_sanitario"],
                                jsonD["data"][i]["categoria_ospiti_rsa"],
                                jsonD["data"][i]["categoria_over80"],
                                jsonD["data"][i]["categoria_personale_scolastico"],
                                jsonD["data"][i]["categoria_forze_armate"],
                                jsonD["data"][i]["prima_dose"],
                                jsonD["data"][i]["seconda_dose"],
                                jsonD["data"][i]["ultimo_aggiornamento"]
                            )
        arrayVaccineSummary.append (vs)

    logManager.writeWithTimestemp ("CalculateResults.py: 'Vaccine Summary' data processed!",suppressConsole )

except Exception as e:
    logManager.writeWithTimestemp ("!! CalculateResults.py: Error on getting 'Vaccine Summary' data... !!",suppressConsole )
    logManager.writeWithTimestemp (str(e),suppressConsole )

totalDoses = 0
totalDosesFirst = 0
totalDosesSecond = 0
for i in range ( len(arrayVaccineSummary) ):
    totalDoses = totalDoses + int(arrayVaccineSummary[i].total)
    totalDosesFirst = totalDosesFirst + int(arrayVaccineSummary[i].first_dose)
    totalDosesSecond = totalDosesSecond + int(arrayVaccineSummary[i].second_dose)

italianPeopleFormatted = locale.format_string("%d", 60360000, grouping=True)
totalDosesFormatted = locale.format_string("%d", totalDoses, grouping=True)
totalDosesFirstFormatted = locale.format_string("%d", totalDosesFirst, grouping=True)
totalDosesSecondFormatted = locale.format_string("%d", totalDosesSecond, grouping=True)

print ("")
print ("")
print ( "=============== TOTALE =====================" )    
print ( "Popolazione Italia: " + italianPeopleFormatted )
print ( "Totale prime dosi somministrate: " + totalDosesFirstFormatted )
print ( "Totale seconde dosi somministrate: " + totalDosesSecondFormatted )
print ( "Totale dosi somministrate: " + totalDosesFormatted )
perPopFirstDose = round((( totalDoses/60360000 ) * 100),2)
#print ( "% Popolazione che ha ricevuto almeno una dose: " + str(perPopFirstDose) )
perPopSecodDose = round((( totalDosesSecond/60360000 ) * 100),2)
print ( "% Popolazione che ha ricevuto 2 dosi - VACCINATA: " + str(perPopSecodDose) )
print ( "Ultimo aggiornamento: " + str (up.last_update) ) 
print ( "=============== TOTALE =====================" )  
print ("")
print ("")

logManager.writeWithTimestemp ("CalculateResults.py: generating pie chart % vaccinated people...",suppressConsole )
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Popolazione vaccinata (prima e sconda dose)', 'Popolazione totale'
sizes = [round(perPopSecodDose,2), round(100-perPopSecodDose,2)]
explode = (0,0.1)  # only "explode" the 2nd slice
fig5, ax1 = plt.subplots()
ax1.grid()
ax1.pie(sizes, explode=explode, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title("Vaccinati " + totalDosesSecondFormatted + " su " + italianPeopleFormatted)
ax1.legend(labels,
          loc="center left",
          bbox_to_anchor=(0, 0, 0, 0))

#plt.show()
logManager.writeWithTimestemp ("CalculateResults.py: pie chart % vaccinated people correctly generated!",suppressConsole )
logManager.writeWithTimestemp ("CalculateResults.py: bar chart % vaccinated people correctly png...",suppressConsole )
plt.savefig(imageOutputPath + 'pie_perc_vaccinated_people.png')  
logManager.writeWithTimestemp ("CalculateResults.py: % vaccinated people correctly png correctly generated!",suppressConsole )


###############################################################################################
# Processing data from 'somministrazioni-vaccini-summary-latest.json' file with defined mapping
###############################################################################################

try:
    arrayAreas = ['ABR','BAS','CAL','CAM','EMR','FVG','LAZ','LIG','LOM','MAR','MOL','PAB','PAT','PIE','PUG','TOS','UMB','VDA','VEN','SAR','SIC']
    #arrayAreas = ['ABR','TOS']

    logManager.writeWithTimestemp ("CalculateResults.py: Getting 'Vaccine Day' data...",suppressConsole )
    jr = JsonRead("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.json")
    
    arrayVaccineItaly = []
    arrayVaccineDayABR = []
    arrayVaccineDayBAS = []
    arrayVaccineDayCAL = []
    arrayVaccineDayCAM = []
    arrayVaccineDayEMR = []
    arrayVaccineDayFVG = []
    arrayVaccineDayLAZ = []
    arrayVaccineDayLIG = []
    arrayVaccineDayLOM = []
    arrayVaccineDayMAR = []
    arrayVaccineDayMOL = []
    arrayVaccineDayPAB = []
    arrayVaccineDayPAT = []
    arrayVaccineDayPIE = []
    arrayVaccineDayPUG = []
    arrayVaccineDayTOS = []
    arrayVaccineDayUMB = []
    arrayVaccineDayVDA = []
    arrayVaccineDayVEN = []
    arrayVaccineDaySAR = []
    arrayVaccineDaySIC = []
    
    TOTDEB = 0
    for a in arrayAreas : 
        logManager.writeWithTimestemp ("Processing vaccine data for area: " + a,suppressConsole )
        jsonD = jr.getDataWithFilter('area',a)
        logManager.writeWithTimestemp ("CalculateResults.py: 'Vaccine Day' data fetched! Processing...",suppressConsole )
        for i in range( len(jsonD) ):
            vd = VaccineDay(    jsonD[i]["index"], 
                                jsonD[i]["data_somministrazione"], 
                                jsonD[i]["totale"]
            )

            if ( a == 'ABR' ):
                arrayVaccineDayABR.append (vd)

            elif ( a == 'BAS'):
                arrayVaccineDayBAS.append (vd)

            elif a == 'CAL':
                arrayVaccineDayCAL.append (vd)

            elif a == 'CAM':
                arrayVaccineDayCAM.append (vd)

            elif a == 'EMR':
                arrayVaccineDayEMR.append (vd)

            elif a == 'FVG':
                arrayVaccineDayFVG.append (vd)

            elif a == 'LAZ':
                arrayVaccineDayLAZ.append (vd)

            elif a == 'LIG':
                arrayVaccineDayLIG.append (vd)

            elif a == 'LOM':
                arrayVaccineDayLOM.append (vd)

            elif a == 'MAR':
                arrayVaccineDayMAR.append (vd)

            elif a == 'MOL':
                arrayVaccineDayMOL.append (vd)

            elif a == 'PAB':
                arrayVaccineDayPAB.append (vd)

            elif a == 'PAT':
                arrayVaccineDayPAT.append (vd)

            elif a == 'PIE':
                arrayVaccineDayPIE.append (vd)

            elif a == 'PUG':
                arrayVaccineDayPUG.append (vd)

            elif a == 'TOS':
                arrayVaccineDayTOS.append (vd)

            elif a == 'UMB':
                arrayVaccineDayUMB.append (vd)

            elif a == 'VDA':
                arrayVaccineDayVDA.append (vd)

            elif a == 'VEN':
                arrayVaccineDayVEN.append (vd)

            elif a == 'SAR':
                arrayVaccineDaySAR.append (vd)

            elif a == 'SIC':
                arrayVaccineDaySIC.append (vd)
         
    arrayVaccineItaly.append(arrayVaccineDayABR)
    arrayVaccineItaly.append(arrayVaccineDayBAS)
    arrayVaccineItaly.append(arrayVaccineDayCAL)
    arrayVaccineItaly.append(arrayVaccineDayCAM)
    arrayVaccineItaly.append(arrayVaccineDayEMR)
    arrayVaccineItaly.append(arrayVaccineDayFVG)
    arrayVaccineItaly.append(arrayVaccineDayLAZ)
    arrayVaccineItaly.append(arrayVaccineDayLIG)
    arrayVaccineItaly.append(arrayVaccineDayLOM)
    arrayVaccineItaly.append(arrayVaccineDayMAR)
    arrayVaccineItaly.append(arrayVaccineDayMOL)
    arrayVaccineItaly.append(arrayVaccineDayPAB)
    arrayVaccineItaly.append(arrayVaccineDayPAT)
    arrayVaccineItaly.append(arrayVaccineDayPUG)
    arrayVaccineItaly.append(arrayVaccineDayPIE)
    arrayVaccineItaly.append(arrayVaccineDayTOS)
    arrayVaccineItaly.append(arrayVaccineDayUMB)
    arrayVaccineItaly.append(arrayVaccineDayVDA)
    arrayVaccineItaly.append(arrayVaccineDayVEN)
    arrayVaccineItaly.append(arrayVaccineDaySAR)
    arrayVaccineItaly.append(arrayVaccineDaySIC)   

    logManager.writeWithTimestemp ("CalculateResults.py: 'Vaccine Day' data processed!",suppressConsole)

except Exception as e:
    logManager.writeWithTimestemp ("!! CalculateResults.py: Error on getting 'Vaccine Day' data... !!",suppressConsole)
    logManager.writeWithTimestemp (str(e) )

DictVaccineTotalForDay = {}
for ar in arrayVaccineItaly:
    for i in ar:
        if not( i.dosing_date in DictVaccineTotalForDay ):
            DictVaccineTotalForDay[i.dosing_date] = i.total
        else:
            DictVaccineTotalForDay[i.dosing_date] = DictVaccineTotalForDay[i.dosing_date] + i.total

ordered_data = sorted(DictVaccineTotalForDay.items(), key = lambda x:datetime.strptime(x[0],'%Y-%m-%dT%H:%M:%S.%f%z') )

logManager.writeWithTimestemp ("=======================================", False)
logManager.writeWithTimestemp ("Vaccine for day:", False)
logManager.writeWithTimestemp (str(ordered_data),False)
logManager.writeWithTimestemp ("=======================================", False)

x = []
y = []
for data in ordered_data:
    date, total = data
    
    '''
    print(date)
    print(total)
    print("---------------")
    '''
    x.append ( 
            datetime ( 
            year=int((date )[0:4]), 
            month=int((date )[5:7]), 
            day=int((date )[8:10]), 
            hour = 0, 
            minute = 0, 
            second = 0 )
    )
    y.append ( total )

logManager.writeWithTimestemp ("CalculateResults.py: generating bar chart Vaccine x Day...",suppressConsole)
fig10, ax1 = plt.subplots()
val = ax1.plot(x,y)
ax1.legend(labels=['Vaccini x Giorni'])
ax1.set(xlabel='Giorni', ylabel='Dosi somministrate', title='Vaccini x Giorni')
ax1.grid()
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=minor_locator_interval))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max_locator_interval))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
ax1.xaxis.set_tick_params(rotation=90)
#for a,b in zip(x, y): 
#    plt.text(a, b, str(b))
#mplcursors.cursor(val) 

#plt.show()
logManager.writeWithTimestemp ("CalculateResults.py: bar chart Vaccine x Day correctly generated",suppressConsole)
logManager.writeWithTimestemp ("CalculateResults.py: bar chart Vaccine x Day generating png...",suppressConsole)
plt.savefig(imageOutputPath + 'bar_chart_vaccine_x_day.png')  
logManager.writeWithTimestemp ("CalculateResults.py: bar chart Vaccine x Day png correctly generated!",suppressConsole)

###############################################################################################
# Processing data from 'dpc-covid19-ita-andamento-nazionale.json' file with defined mapping
###############################################################################################
try:
    logManager.writeWithTimestemp ("CalculateResults.py: Getting 'Covid19' general data...",suppressConsole)
    jr = JsonRead("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json")
    arrayCovid19Data = []
    jsonD = jr.getData()
    logManager.writeWithTimestemp ("CalculateResults.py: 'Covid19' data fetched! Processing...",suppressConsole)
    for i in range( len(jsonD)-intervalDay, len(jsonD), 1):
        C19Ds = Covid19DataSet(    
                            jsonD[i]["data"], 
                            jsonD[i]["ricoverati_con_sintomi"], 
                            jsonD[i]["terapia_intensiva"],
                            jsonD[i]["totale_ospedalizzati"],
                            jsonD[i]["totale_positivi"],
                            jsonD[i]["variazione_totale_positivi"],
                            jsonD[i]["nuovi_positivi"],
                            jsonD[i]["dimessi_guariti"],
                            jsonD[i]["deceduti"],
                            jsonD[i]["totale_casi"],
                            jsonD[i]["tamponi"]
        )
        arrayCovid19Data.append (C19Ds)

    logManager.writeWithTimestemp ("CalculateResults.py: 'Covid19' data processed!",suppressConsole)

except Exception as e:
    logManager.writeWithTimestemp ("!! CalculateResults.py: Error on getting 'Covid19' data... !!",suppressConsole)
    logManager.writeWithTimestemp (str(e),suppressConsole)

print ("=============== CASI x GIORNO =================" )

x = [] #date
y = [] #%positive
z = [] #death
t = [] #terapie intensive
o = [] #ospedalizzati

for i in range ( 1,len(arrayCovid19Data) ):
    x.append ( 
            datetime ( 
            year=int((arrayCovid19Data[i].data )[0:4]), 
            month=int((arrayCovid19Data[i].data )[5:7]), 
            day=int((arrayCovid19Data[i].data )[8:10]), 
            hour = 0, 
            minute = 0, 
            second = 0 )
    )
    
    #calculating delta that are not present on data from GIT
    deltaTamponi = 0
    deltaDeceduti = 0
    deltaTamponi = arrayCovid19Data[i].tamponi - arrayCovid19Data[i-1].tamponi
    deltaDeceduti = arrayCovid19Data[i].deceduti - arrayCovid19Data[i-1].deceduti

    percPos = round( arrayCovid19Data[i].nuovi_pos/deltaTamponi,3)
    #fixing error on data from GIT
    #17/12/2020 wrong number of tamponi...
    if ( (arrayCovid19Data[i].data[8:10] == '17')  and (arrayCovid19Data[i].data[5:7]) == '12' and (arrayCovid19Data[i].data[0:4] == '2020' ) ):
        percPos = 0.09
    #fixing error on data from GIT
    y.append ( percPos )
    z.append ( deltaDeceduti )
    t.append ( arrayCovid19Data[i].ti )
    o.append ( arrayCovid19Data[i].tot_osp ) 

    print ( str(arrayCovid19Data[i].data)   + " -> TOT:" + str(arrayCovid19Data[i].tot_casi) 
                                            + " - NEW:" + str(arrayCovid19Data[i].nuovi_pos) 
                                            + " - TAMPONI TOT:" + str(arrayCovid19Data[i].tamponi) 
                                            + " - TAMPONI DAY:" + str(deltaTamponi) 
                                            + " - %POS: " + str( percPos ) 
                                            + " - DEC: " + str( deltaDeceduti ) 
                                            + " - TI TOT: " + str( arrayCovid19Data[i].ti ) 
                                            + " - OSPEDALIZZATI: " + str( arrayCovid19Data[i].tot_osp ) 
    )
'''
p7 = [] #%positive7dayAver
for i in range (1,8):
    p7.append(0)

for i in range ( 1,len(y) ):
    if ( i >= 7 ):
        avr7 = 0.0
        for j in range (7,1,-1):
            avr7 += y[i-j]
            #print(">>>>>1: " + str(avr7) )
        avr7 = avr7/7
        #print(">>>>>2: " + str(avr7) )
        p7.append (avr7)
'''

###############################################################################################
# Processing data from 'dpc-covid19-ita-province.json' - PROVINCE
###############################################################################################
try:
    logManager.writeWithTimestemp ("CalculateResults.py: Getting 'Covid19 Province'...",suppressConsole)
    jr = JsonRead("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json")
    arrayCovid19DataProv = []
    jsonD = jr.getDataWithFilterPROV('sigla_provincia',"PO")
    logManager.writeWithTimestemp ("CalculateResults.py: 'Covid19 Province' data fetched! Processing...",suppressConsole)
    for i in range( len(jsonD)-intervalDay, len(jsonD), 1):
        C19DPr = Covid19DataSetProv(    
                            jsonD[i]["data"], 
                            jsonD[i]["stato"], 
                            jsonD[i]["codice_regione"],
                            jsonD[i]["denominazione_regione"],
                            jsonD[i]["codice_provincia"],
                            jsonD[i]["denominazione_provincia"],
                            jsonD[i]["sigla_provincia"],
                            jsonD[i]["totale_casi"],
        )
        arrayCovid19DataProv.append (C19DPr)

    logManager.writeWithTimestemp ("CalculateResults.py: 'Covid19 Provincia' data processed!",suppressConsole)

except Exception as e:
    logManager.writeWithTimestemp ("!! CalculateResults.py: Error on getting 'Covid19 Provincia' data... !!",suppressConsole)
    logManager.writeWithTimestemp (str(e),suppressConsole)

xp = [] #date
yp = [] #cases
oldCases = arrayCovid19DataProv[0].tot_casi #only total cases for day are released.
deltaCases = 0
Provincia = arrayCovid19DataProv[0].den_pro

print ( "CASI/GIORNO PER " + Provincia)
for i in range ( 2,len(arrayCovid19DataProv) ):
    xp.append ( 
            datetime ( 
            year=int((arrayCovid19DataProv[i].data )[0:4]), 
            month=int((arrayCovid19DataProv[i].data )[5:7]), 
            day=int((arrayCovid19DataProv[i].data )[8:10]), 
            hour = 0, 
            minute = 0, 
            second = 0 )
    )
    deltaCases = arrayCovid19DataProv[i].tot_casi - oldCases
    oldCases = arrayCovid19DataProv[i].tot_casi
    yp.append ( deltaCases )

    print ( str(arrayCovid19DataProv[i].data)   + " -> CASI DAY:" + str(deltaCases) )

###############################################################################################

logManager.writeWithTimestemp ("CalculateResults.py: generating plot chart 'Covid19 %positive'...",suppressConsole)
fig15, ax1 = plt.subplots()
ax1.plot(x,y)
ax1.legend(labels=['% Positivi (casi/tamponi)'])
ax1.set(xlabel='Giorni', ylabel='%Positivi', title='% Positivi (casi/tamponi)')
ax1.grid()
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=minor_locator_interval))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max_locator_interval))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
ax1.xaxis.set_tick_params(rotation=90)
logManager.writeWithTimestemp ("CalculateResults.py: bar chart 'Covid19 %positive' correctly generated",suppressConsole)
#plt.show()
logManager.writeWithTimestemp ("CalculateResults.py: plot chart %positive gereating png...",suppressConsole)
plt.savefig(imageOutputPath + 'plot_perc_positive.png')  
logManager.writeWithTimestemp ("CalculateResults.py: plot chart %positive png correctly generated!",suppressConsole)

logManager.writeWithTimestemp ("CalculateResults.py: generating plot chart 'Covid 19 death'...",suppressConsole)
fig20, ax1 = plt.subplots()
ax1.plot(x,z)
ax1.legend(labels=['Deceduti x Giorno'])
ax1.set(xlabel='Giorni', ylabel='Deceduti', title='Deceduti x Giorno')
ax1.grid()
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=minor_locator_interval))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max_locator_interval))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
ax1.xaxis.set_tick_params(rotation=90)
#plt.show()
logManager.writeWithTimestemp ("CalculateResults.py: bar chart 'Covid 19 death' correctly generated",suppressConsole)
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Covid 19 death' gereating png...",suppressConsole)
plt.savefig(imageOutputPath + 'plot_death.png')  
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Covid 19 death' png correctly generated!",suppressConsole)

logManager.writeWithTimestemp ("CalculateResults.py: generating plot chart 'Covid 19 TI'...",suppressConsole)
fig20, ax1 = plt.subplots()
ax1.plot(x,t)
ax1.legend(labels=['Terapie Intensive'])
ax1.set(xlabel='Giorni', ylabel='Deceduti', title='Terapie Intensive')
ax1.grid()
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=minor_locator_interval))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max_locator_interval))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
ax1.xaxis.set_tick_params(rotation=90)
logManager.writeWithTimestemp ("CalculateResults.py: bar chart 'Terapie Intensive' correctly generated",suppressConsole)
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Terapie Intensive' gereating png...",suppressConsole)
plt.savefig(imageOutputPath + 'plot_terapie_intensive_.png')  
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Terapie Intensive' png correctly generated!",suppressConsole)

logManager.writeWithTimestemp ("CalculateResults.py: generating plot chart 'Terapie Intensive'...",suppressConsole)
fig20, ax1 = plt.subplots()
ax1.plot(x,o)
ax1.legend(labels=['Ospedalizzati'])
ax1.set(xlabel='Giorni', ylabel='Ospedalizzati', title='Ospedalizzati')
ax1.grid()
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=minor_locator_interval))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max_locator_interval))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
ax1.xaxis.set_tick_params(rotation=90)
logManager.writeWithTimestemp ("CalculateResults.py: bar chart 'Ospedalizzati' correctly generated",suppressConsole)
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Ospedalizzati' gereating png...",suppressConsole)
plt.savefig(imageOutputPath + 'plot_ospedalizzati_.png')  
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Ospedalizzati' png correctly generated!",suppressConsole)

logManager.writeWithTimestemp ("============================================================================",False)
logManager.writeWithTimestemp ("Last Update: " + str (up.last_update), False )
logManager.writeWithTimestemp ("============================================================================",False)