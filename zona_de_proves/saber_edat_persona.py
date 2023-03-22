from datetime import date, datetime
import json

def calcular_edat(data_naixement):
    edat = 0
    today = date.today()
    edat = today.year - data_naixement.year - ((today.month, today.day) < (data_naixement.month, data_naixement.day))
    return edat

with open("./dades_personals.json") as fitxer_2:
    dades = json.load(fitxer_2)
    for persona in dades['Persones']:
        #funció per convertir string en day,month,year
        dt = datetime.strptime(persona['data_naixement'], '%d/%m/%Y')  
        #per accedir al contingut: dt.day, dt.month, dt.year  
        print(calcular_edat(date(dt.year,dt.month,dt.day)))