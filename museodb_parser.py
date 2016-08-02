#! python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 14:20:22 2016

@author: Fritz
"""
from bs4 import BeautifulSoup
import requests,csv#,pyperclip

restart= True
print('Campos de busqueda:\n[1]Coleccion\n[2]Orden\n[3]Familia\n[4]Genero o Especie')
while restart:    
    Coleccion = input('Coleccion: ')
    Orden = input('Orden: ')
    Familia = input('Familia: ')
    Gen_Especie = input('Genero o Especie: ')
    Submit = input('Escriba si para buscar: ')
    if Submit.lower() != 'si':
        continue
    else:
        url ='http://www.mnhn.gov.do/Visualizar_Registros.php?id_grupo=%s&id_orden=%s&cod_familia=%s&cod_especie=%s&cod_restriccion=-1'%(Coleccion,Orden,Familia,Gen_Especie)
        #url= pyperclip.paste()# Alternative to copy url from clipboard
        r =requests.get(url)
        soup = BeautifulSoup(r.content,"lxml")
        #all_records =[]# Used for troubleshooting    
        if soup.find_all('table',class_='ic-grid') == []:
            print('Resultados no encontrados en la base de datos')        
        else:
            restart = False
            outputname = input('Output Name: ')
            with open(outputname+'.csv', 'w',newline = '') as csvfile:
                fieldnames = ['Coleccion',
                          'Orden',
                          'Familia',
                          'Genero',
                          'Especie',
                          'Nombre_Comun',
                          'Medio_Conservacion',
                          'Restriccion_Geografica',
                          'Pais',
                          'Provincia',
                          'Municipio'
                          ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()    
                for i in soup.find_all('table',class_='ic-grid'):
                    a =[]#record list
                    for r in i.find_all('td'):
                        a.append(r.text.strip())
                    #a.append(r.text.encode('latin-1'))
                    b = a[0].split() #list of words of the first record
                    if len(b) >=5:
                        record ={'Coleccion': b[1].capitalize(),
                             'Orden': a[2].capitalize(),
                             'Familia': a[4].capitalize(),
                             'Genero': a[6].capitalize(),
                             'Especie': b[4].lower(),
                             'Nombre_Comun': a[8].capitalize(),
                             'Medio_Conservacion': a[10].capitalize(),
                             'Restriccion_Geografica': a[12].capitalize(),
                             'Pais': a[14].title(),
                             'Provincia': a[16].title(),
                             'Municipio': a[18].title()
                             }
                    else:
                        record ={'Coleccion': b[1].capitalize(),
                             'Orden': a[2].capitalize(),
                             'Familia': a[4].capitalize(),
                             'Genero': a[6].capitalize(),
                             'Especie': None,
                             'Nombre_Comun': a[8].capitalize(),
                             'Medio_Conservacion': a[10].capitalize(),
                             'Restriccion_Geografica': a[12].capitalize(),
                             'Pais': a[14].title(),
                             'Provincia': a[16].title(),
                             'Municipio': a[18].title()
                             }
                    writer.writerow(record)
                    #all_records.append(record)#Used for troubleshooting
