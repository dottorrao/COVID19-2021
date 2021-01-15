from Json import JsonRead
from Log import LogManager
import pathlib
from VaccineSummary import VaccineSummary
from VaccineDay import VaccineDay
from Covid19DataSet import Covid19DataSet
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from Update import Update
import configparser 

logManager = LogManager (pathlib.Path().absolute(),"Covid19-2021.log","debug")
logManager.writeWithTimestemp ("=============================")
logManager.writeWithTimestemp ("=  CalculateResults module  =")
logManager.writeWithTimestemp ("=============================")

configParser = configparser.RawConfigParser()   
configFilePath = r'./config.ini'
configParser.read(configFilePath)

intervalDay = int ( configParser.get('interval', 'dayInterval') )
minor_locator_interval = int ( configParser.get('interval', 'minor_locator_interval') )
max_locator_interval = int ( configParser.get('interval', 'max_locator_interval') )

#########################################################################################
# Processing data from 'anagrafica-vaccini-summary-latest.json' file with defined mapping
#########################################################################################

#getting last update timestamp
jr = JsonRead("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/last-update-dataset.json")
jsonD = jr.getData()
up = Update (jsonD["ultimo_aggiornamento"])

arrayVaccineSummary = []
try:
    logManager.writeWithTimestemp ("CalculateResults.py: Getting 'Vaccine Summary' data...")
    jr = JsonRead("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.json")
    jsonD = jr.getData()
    logManager.writeWithTimestemp ("CalculateResults.py: 'Vaccine Summary' data fetched! Processing...")
    for i in range( len(jsonD["data"]) ):
        vs = VaccineSummary(    jsonD["data"][i]["index"], 
                                jsonD["data"][i]["fascia_anagrafica"],
                                jsonD["data"][i]["totale"],
                                jsonD["data"][i]["sesso_maschile"],
                                jsonD["data"][i]["sesso_femminile"],
                                jsonD["data"][i]["categoria_operatori_sanitari_sociosanitari"],
                                jsonD["data"][i]["categoria_personale_non_sanitario"],
                                jsonD["data"][i]["categoria_ospiti_rsa"],
                                jsonD["data"][i]["ultimo_aggiornamento"],
                            )
        arrayVaccineSummary.append (vs)

    logManager.writeWithTimestemp ("CalculateResults.py: 'Vaccine Summary' data processed!")

except Exception as e:
    logManager.writeWithTimestemp ("!! CalculateResults.py: Error on getting 'Vaccine Summary' data... !!")
    logManager.writeWithTimestemp (str(e))

total = 0
for i in range ( len(arrayVaccineSummary) ):
    total = total + int(arrayVaccineSummary[i].total)

print ("")
print ("")
print ( "=============== TOTALE =====================" )    
print ( "Totale vaccini eseguiti: " + str(total) )
print ( "Popolazione Italia: 60.360.000")
perPopVac = round((( total/60360000 ) * 100),2)
print ( "% Popolazione vaccinata:" + str(perPopVac) )
print ( "=============== TOTALE =====================" )  
print ("")
print ("")

logManager.writeWithTimestemp ("CalculateResults.py: generating pie chart % vaccinated people...")
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Popolazione vaccinata', 'Popolazione totale'
sizes = [round(perPopVac,2), round(100-perPopVac,2)]
explode = (0,0.1)  # only "explode" the 2nd slice
fig5, ax1 = plt.subplots()
ax1.grid()
ax1.pie(sizes, explode=explode, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title("Vaccinati " + str(total) + " su 60360000")
ax1.legend(labels,
          loc="center left",
          bbox_to_anchor=(0, 0, 0, 0))

#plt.show()
logManager.writeWithTimestemp ("CalculateResults.py: pie chart % vaccinated people correctly generated!")
logManager.writeWithTimestemp ("CalculateResults.py: bar chart % vaccinated people correctly png...")
plt.savefig('/Users/marco/Desktop/outPutCovidGraph/pie_perc_vaccinated_people.png')  
logManager.writeWithTimestemp ("CalculateResults.py: % vaccinated people correctly png correctly generated!")

###############################################################################################
# Processing data from 'somministrazioni-vaccini-summary-latest.json' file with defined mapping
###############################################################################################

try:
    logManager.writeWithTimestemp ("CalculateResults.py: Getting 'Vaccine Day' data...")
    jr = JsonRead("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.json")
    arrayVaccineDay = []
    jsonD = jr.getDataWithFilter('area','ITA')

    logManager.writeWithTimestemp ("CalculateResults.py: 'Vaccine Day' data fetched! Processing...")
    for i in range( len(jsonD) ):
        vd = VaccineDay(    jsonD[i]["index"], 
                            jsonD[i]["data_somministrazione"], 
                            jsonD[i]["totale"]
        )
        arrayVaccineDay.append (vd)

    logManager.writeWithTimestemp ("CalculateResults.py: 'Vaccine Day' data processed!")

except Exception as e:
    logManager.writeWithTimestemp ("!! CalculateResults.py: Error on getting 'Vaccine Day' data... !!")
    logManager.writeWithTimestemp (str(e))
print ("")
print ("")
print ("=============== PER GIORNI =================" ) 
total = 0
x = []
y = []
for i in range ( 0,len(arrayVaccineDay) ):
    x.append ( 
            datetime ( 
            year=int((arrayVaccineDay[i].dosing_date )[0:4]), 
            month=int((arrayVaccineDay[i].dosing_date )[5:7]), 
            day=int((arrayVaccineDay[i].dosing_date )[8:10]), 
            hour = 0, 
            minute = 0, 
            second = 0 )
    )
    y.append ( arrayVaccineDay[i].total )
    
    total = total + int( arrayVaccineDay[i].total )
    print ( str(arrayVaccineDay[i].dosing_date) + " -> " + str(arrayVaccineDay[i].total) )

print ("TOTAL -> " + str(total) )
print ("=============== PER GIORNI =================" )
print ("")
print ("")

logManager.writeWithTimestemp ("CalculateResults.py: generating bar chart Vaccine x Day...")
fig10, ax1 = plt.subplots()
ax1.bar(x,y)
ax1.legend(labels=['Vaccini x Giorni'])
ax1.set(xlabel='Giorni', ylabel='Dosi somministrate', title='Vaccini x Giorni')
ax1.grid()
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=minor_locator_interval))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max_locator_interval))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
ax1.xaxis.set_tick_params(rotation=90)
#plt.show()
logManager.writeWithTimestemp ("CalculateResults.py: bar chart Vaccine x Day correctly generated")
logManager.writeWithTimestemp ("CalculateResults.py: bar chart Vaccine x Day generating png...")
plt.savefig('/Users/marco/Desktop/outPutCovidGraph/bar_chart_vaccine_x_day.png')  
logManager.writeWithTimestemp ("CalculateResults.py: bar chart Vaccine x Day png correctly generated!")

###############################################################################################
# Processing data from 'dpc-covid19-ita-andamento-nazionale.json' file with defined mapping
###############################################################################################
try:
    logManager.writeWithTimestemp ("CalculateResults.py: Getting 'Covid19' general data...")
    jr = JsonRead("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json")
    arrayCovid19Data = []
    jsonD = jr.getData()
    logManager.writeWithTimestemp ("CalculateResults.py: 'Covid19' data fetched! Processing...")
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

    logManager.writeWithTimestemp ("CalculateResults.py: 'Covid19' data processed!")

except Exception as e:
    logManager.writeWithTimestemp ("!! CalculateResults.py: Error on getting 'Covid19' data... !!")
    logManager.writeWithTimestemp (str(e))

print ("=============== CASI x GIORNO =================" )

x = [] #date
y = [] #%positive
z = [] #death
t = [] #terapie intensive

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

    percPos = round( arrayCovid19Data[i].nuovi_pos/deltaTamponi,2)
    #fixing error on data from GIT
    #17/12/2020 wrong number of tamponi...
    if ( (arrayCovid19Data[i].data[8:10] == '17')  and (arrayCovid19Data[i].data[5:7]) == '12' and (arrayCovid19Data[i].data[0:4] == '2020' ) ):
        percPos = 0.09
    #fixing error on data from GIT
    y.append ( percPos )
    z.append ( deltaDeceduti )
    t.append ( arrayCovid19Data[i].ti )

    print ( str(arrayCovid19Data[i].data)   + " -> TOT:" + str(arrayCovid19Data[i].tot_casi) 
                                            + " - NEW:" + str(arrayCovid19Data[i].nuovi_pos) 
                                            + " - TAMPONI TOT:" + str(arrayCovid19Data[i].tamponi) 
                                            + " - TAMPONI DAY:" + str(deltaTamponi) 
                                            + " - %POS: " + str( percPos ) 
                                            + " - DEC: " + str( deltaDeceduti ) 
                                            + " - TI TOT: " + str( arrayCovid19Data[i].ti ) 
    )

logManager.writeWithTimestemp ("CalculateResults.py: generating plot chart 'Covid19 %positive'...")
fig15, ax1 = plt.subplots()
ax1.plot(x,y)
ax1.legend(labels=['% Positivi (casi/tamponi)'])
ax1.set(xlabel='Giorni', ylabel='%Positivi', title='% Positivi (casi/tamponi)')
ax1.grid()
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=minor_locator_interval))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max_locator_interval))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
ax1.xaxis.set_tick_params(rotation=90)
logManager.writeWithTimestemp ("CalculateResults.py: bar chart 'Covid19 %positive' correctly generated")
#plt.show()
logManager.writeWithTimestemp ("CalculateResults.py: plot chart %positive gereating png...")
plt.savefig('/Users/marco/Desktop/outPutCovidGraph/plot_perc_positive.png')  
logManager.writeWithTimestemp ("CalculateResults.py: plot chart %positive png correctly generated!")

logManager.writeWithTimestemp ("CalculateResults.py: generating plot chart 'Covid 19 death'...")
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
logManager.writeWithTimestemp ("CalculateResults.py: bar chart 'Covid 19 death' correctly generated")
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Covid 19 death' gereating png...")
plt.savefig('/Users/marco/Desktop/outPutCovidGraph/plot_death.png')  
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Covid 19 death' png correctly generated!")

logManager.writeWithTimestemp ("CalculateResults.py: generating plot chart 'Covid 19 TI'...")
fig20, ax1 = plt.subplots()
ax1.plot(x,t)
ax1.legend(labels=['Terapie Intensive'])
ax1.set(xlabel='Giorni', ylabel='Deceduti', title='Terapie Intensive')
ax1.grid()
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=minor_locator_interval))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max_locator_interval))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
ax1.xaxis.set_tick_params(rotation=90)
#plt.show()
logManager.writeWithTimestemp ("CalculateResults.py: bar chart 'Terapie Intensive' correctly generated")
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Terapie Intensive' gereating png...")
plt.savefig('/Users/marco/Desktop/outPutCovidGraph/plot_Terapie_Intensive.png')  
logManager.writeWithTimestemp ("CalculateResults.py: plot chart 'Terapie Intensive' png correctly generated!")

logManager.writeWithTimestemp ("============================================================================")
logManager.writeWithTimestemp ("Last Update: " + str (up.last_update) )
logManager.writeWithTimestemp ("============================================================================")