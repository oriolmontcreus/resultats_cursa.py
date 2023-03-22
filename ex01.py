#DNI = 41589407w
# N = (D+A+M) mod 5
# N = (07+04+06) mod 5 = 2 ---------> RESULTATS D’UNA CURSA

#Menú fet amb inquirer
#https://python-inquirer.readthedocs.io/en/latest/examples.html

import os
import json
from datetime import date, datetime
import inquirer
from colorama import init, Fore
init(autoreset=True) #Autoreset dels colors del colorama (per a més control del color)

FILE_CLASSIFICACIO = "./classificacio.json"
FILE_DADES_PERSONALS = "./dades_personals.json"
dades = []
classificacio = []

#Obrir els fitxers a l'inici del programa
def obrir_fitxers():
    #Obrim i carreguem els dos fitxers
    with open(FILE_CLASSIFICACIO) as fitxer_1:
        classificacio = json.load(fitxer_1)
        fitxer_1.close()
    
    with open(FILE_DADES_PERSONALS) as fitxer_2:
        dades = json.load(fitxer_2)
        fitxer_2.close()    
    return classificacio, dades

#Afegir informació al fitxer de dades personals
def afegir_a_fitxer_dades(noves_dades, nom_fitxer='dades_personals.json'):
    with open(nom_fitxer,'r+') as fitxer:
        # Carregar les dades en un diccionari "dades_fitxer"
        dades_fitxer = json.load(fitxer)
        # Ajuntar la informació nova amb la vella
        dades_fitxer["Persones"].append(noves_dades)
        # Sets file's current position at offset.
        fitxer.seek(0)
        # convert back to json.
        json.dump(dades_fitxer, fitxer, indent = 4)
     
#Submenú per l'apartat de classificacions
def submenu_classificacions(classificacio, dades):
    os.system('cls') #Esborrar el contingut anterior de la consola
    opcions_submenu = [
        inquirer.List('submenu_classificacions',
                      message="Tria una opció del submenú",
                      choices=['Classificació global', 'Classificació menors de 10 anys', 'Classificació majors de 70 anys'],
                      ),
    ]
    respostes_submenu = inquirer.prompt(opcions_submenu)
    
    if respostes_submenu['submenu_classificacions'] == 'Classificació global':
        imprimir_classificacio(dades, (classificacions(classificacio, dades, 999)))
    
    if respostes_submenu['submenu_classificacions'] == 'Classificació menors de 10 anys':
        imprimir_classificacio(dades, (classificacions(classificacio, dades, 10)))
            
    if respostes_submenu['submenu_classificacions'] == 'Classificació majors de 70 anys':
        imprimir_classificacio(dades, (classificacions(classificacio, dades, 70)))

#Funcions relacionades amb la validació d'un dni
def comprovar_digits(n):
    contador_digits = 0
    if n == 0: 
        contador = 1
    else:
        contador = 1
        while (n>=10):
            contador += 1
            n = n//10
        return contador
def validar_dni():
    while True:
        try:
            dni_sense_lletra = int(input("[" + Fore.YELLOW + "?" + Fore.RESET + "] " + "Entra el dni (sense la última lletra): "))
            if comprovar_digits(dni_sense_lletra) != 8:
                print(Fore.RED + "[!] Error [!] " + Fore.YELLOW +  "Has d'entrar 8 digits!")
                print("")
                continue # Tornar a començar el loop
        except ValueError: #Exepció quan l'usuari no entra un int
            print(Fore.RED + "[!] Error [!] " + Fore.YELLOW + "Només s'admeten nombres!")
            print("")
            continue # Tornar a començar el loop
        
            # el dni entrat és vàlid
        return dni_sense_lletra
    
#Buscar la lletra del dni entrat    
def trobar_lletra(dni_sense_lletra):
    
    diccionari_lletres = {0:"T",1:"R",2:"W",3:"A",4:"G",5:"M",6:"Y",7:"F",8:"P",9:"D",10:"X",
               11:"B",12:"N",13:"J",14:"Z",15:"S",16:"Q",17:"V",18:"H",19:"L",
               20:"C",21:"K",22:"E"}
    
    resta = dni_sense_lletra%23
    lletra = diccionari_lletres[resta]
    dni = str(dni_sense_lletra) + lletra
    return dni

#Buscar el dorsal amb el valor màxim del fitxer dades_personals.json i afegir-li +1
def trobar_dorsal_disponible(dades):
    #Retorna les dades de una persona amb el valor de dorsal més gran
    persona = max(dades['Persones'], key=lambda ev: int(ev['dorsal']))
    #De la persona trobada anteriorment, només retorna el camp dorsal + 1
    dorsal_disponible = int(persona['dorsal']) + 1
    return dorsal_disponible

#Preguntar per la data de naixement i validar que estigui amb el format que toca, retorna la data en format string
def validar_data_naixement(): 
    while True:
        try:
            raw_data_naixement = input("[" + Fore.YELLOW + "?" + Fore.RESET + "] " + "Entra la data de naixement en el format DD/MM/YYYY: ")
            data_naixement_valida = datetime.strptime(raw_data_naixement, '%d/%m/%Y')
        except ValueError:
            print(Fore.RED + "[!] Format incorrecte, hauria de ser DD-MM-YYY")
            continue
        return str(data_naixement_valida.day) + "/" + str(data_naixement_valida.month) + "/" + str(data_naixement_valida.year)

#Donar d'alta una persona en dades_personals.json
def donar_alta(dades):
    os.system('cls') #Esborrar contingut anterior de la consola
    dorsal = str(trobar_dorsal_disponible(dades))
    dni = trobar_lletra(validar_dni())
    preguntes = [
    inquirer.Text("v_nom", message="Entra el nom"),
    inquirer.Text("v_cognom1", message="Entra el primer cognom"),
    inquirer.Text("v_cognom2", message="Entra el segon cognom"),
    ]

    respostes = inquirer.prompt(preguntes)
    
    noves_dades = {
	    "dni": dni,
        "nom": respostes['v_nom'].capitalize(),
        "cognoms": respostes['v_cognom1'].capitalize() + " " + respostes['v_cognom2'].capitalize(),
        "data_naixement": validar_data_naixement(),
        "dorsal": dorsal
	     }
    
    afegir_a_fitxer_dades(noves_dades)

#Buscar el nom i cognoms de una persona segons el seu dorsal
def buscar_nom(dades, dorsal_persona):
    for persona in dades['Persones']:
        if persona['dorsal'] == dorsal_persona:
            return persona['nom'] + " " + persona['cognoms']

#Donar format al temps de la classificació
def format_temps_classificacio(segons):
    segons = int(segons)
    minuts = segons / 60

    hores = minuts / 60
    minuts_restants = round((hores - (minuts // 60)) * 60)
    segons_restants = round((minuts - (segons // 60)) * 60)

    return('{:02}'.format(round(minuts // 60)) + "h " + ('{:02}'.format(minuts_restants)) + "min " + '{:02}'.format(segons_restants) + "s")

#Imprimir la classificació en un format bonic
def imprimir_classificacio(dades, classificacio):
    i = 0
    print(Fore.BLUE + "────Classificació Global────")
    for dorsal, timestamp in classificacio:
        i += 1
        #Mostrar símbol de medalla pels corredors del podium (top 3)
        match (i):
            case 1:
                print(u"\U0001F947 " + Fore.GREEN + buscar_nom(dades, dorsal).ljust(25), "Temps: ", format_temps_classificacio(timestamp))
            case 2:
                print(u"\U0001F948 " + Fore.GREEN + buscar_nom(dades, dorsal).ljust(25), "Temps: ", format_temps_classificacio(timestamp))
            case 3:
                print(u"\U0001F949 " + Fore.GREEN + buscar_nom(dades, dorsal).ljust(25), "Temps: ", format_temps_classificacio(timestamp))
                
        #Mostrar temps del corredors que no estàn en el top 3
        if i > 3:        
            print(" "+ str(i)+ " " + Fore.GREEN + buscar_nom(dades, dorsal).ljust(25), "Temps: ", format_temps_classificacio(timestamp))

#Classificar segons dorsal i edat
def dorsal_edat(buscar_edat, dorsal_persona, dades):
    
    match (buscar_edat):
        case 10:
            for persona in dades['Persones']:
                if persona['dorsal'] == dorsal_persona and calcular_edat(persona['data_naixement']) < buscar_edat:
                    return calcular_edat(persona['data_naixement'])
        case 70:
            for persona in dades['Persones']:
                if persona['dorsal'] == dorsal_persona and calcular_edat(persona['data_naixement']) > buscar_edat:
                    return calcular_edat(persona['data_naixement'])
     
#Mostrar classsificació segons la id_cerca que rep la funció        
def classificacions(classificacio, dades, id_cerca = 999):
    dorsal_persona = ''
    my_dict_full = {}
    my_dict_10 = {}
    my_dict_70 = {}
    if id_cerca == 999: #Classificació de totes les persones
        for control in classificacio['Controls']:
            if control['descripcio']=='Meta':
                for dorsal in control['dorsals']:
                    dorsal_persona = dorsal['dorsal']
                    my_dict_full[dorsal_persona] = dorsal['timestamp']
        sorted_my_dict = sorted(my_dict_full.items(), key=lambda x:x[1])
                
    if id_cerca == 10: #Classificació de menors de 10 anys
        for control in classificacio['Controls']:
            if control['descripcio']=='Meta':
                for dorsal in control['dorsals']:
                    dorsal_persona = dorsal['dorsal']
                    if dorsal_edat(10,dorsal_persona, dades):
                        my_dict_10[dorsal_persona] = dorsal['timestamp']
        sorted_my_dict = sorted(my_dict_10.items(), key=lambda x:x[1])
                
    if id_cerca == 70: #Classificació de majors de 70 anys
        for control in classificacio['Controls']:
            if control['descripcio']=='Meta':
                for dorsal in control['dorsals']:
                    dorsal_persona = dorsal['dorsal']
                    if dorsal_edat(70,dorsal_persona, dades):
                        my_dict_70[dorsal_persona] = dorsal['timestamp']
                
        sorted_my_dict = sorted(my_dict_70.items(), key=lambda x:x[1])
        
    return sorted_my_dict

#Funcions per a calcular l'edat
def calcular_edat(data_naixement):
    edat = 0
    today = date.today()
    dt = datetime.strptime(data_naixement, '%d/%m/%Y')  
    edat = today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))
    return edat

#Submenú per l'apartat de volcar classificacions
def submenu_volcar(classificacio, dades):
    os.system('cls') #Esborrar el contingut anterior de la consola
    opcions_submenu = [
        inquirer.List('submenu_volcar',
                      message="Tria una opció del submenú",
                      choices=['Classificació global', 'Classificació menors de 10 anys', 'Classificació majors de 70 anys'],
                      ),
    ]
    respostes_submenu = inquirer.prompt(opcions_submenu)
    
    if respostes_submenu['submenu_volcar'] == 'Classificació global':
        imprimir_classificacio(dades, volcar_classificacions(dades, classificacio, 999))
    
    if respostes_submenu['submenu_volcar'] == 'Classificació menors de 10 anys':
        volcar_classificacions(dades, classificacio, 10)
            
    if respostes_submenu['submenu_volcar'] == 'Classificació majors de 70 anys':
        volcar_classificacions(dades, classificacio, 70)

def volcar_classificacions(dades, classificacio, id_edat):
    
    match (id_edat):
        case 999:
            classificacio(classificacio, dades, 999)
        case 70:
            classificacio(classificacio, dades, 70)
        case 10:
            classificacio(classificacio, dades, 10)
          
def main():
    classificacio, dades = obrir_fitxers()
    print(
        Fore.BLUE + """
    │━━━━━━━━━━━━━━━━━━━━━━━│
    │ Resultats d'una cursa │
    │━━━━━━━━━━━━━━━━━━━━━━━│
    """, Fore.YELLOW + """fet per: Oriol Mont\n"""
    )
    while True:
        print(Fore.RED + "━━━━━━━━━━━━━━━━━━━━━━━")
        opcions = [
            inquirer.List('menu_principal',
                        message="Tria una opció del menú",
                        choices=['Classificacions', 'Volcar classificacions', 'Donar d`alta una persona', 'Sortir del programa'],
                        ),
        ]
        respostes = inquirer.prompt(opcions)
        
        if respostes['menu_principal'] == 'Classificacions':
            submenu_classificacions(classificacio, dades)
            continue
        if respostes['menu_principal'] == 'Donar d`alta una persona':
            donar_alta(dades)
            continue
        if respostes['menu_principal'] == 'Volcar classificacions':
            volcar_classificacions(dades, classificacio)
            continue
        if respostes['menu_principal'] == 'Sortir del programa':
            break

main()