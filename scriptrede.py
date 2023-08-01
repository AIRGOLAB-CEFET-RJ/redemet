#Cada solicitação permite buscar o equivalente a 8.760 registros aproximadamente.
#Há disponibilidade de mensagens desde 01/01/2003 até a presente data.
#COVAK ou NSC é usado para substituir as informações sobre visibilidade, alcance,visual na pista, tempo presente, nuvens e visibilidade vertical quando ocorrerem, simultaneamente, no momento da observação, as seguintes condições: visibilidade: 10 km ou mais, em todo o horizonte; nenhuma nuvem de significado operacional; nenhum fenômeno meteorológico significativo
#COR aparece quando ocorre uma correção do uniforme
#METAR Informe meteorológico regular de aeródromo. Utilizado para a descrição completa das condições meteorológicas observadas em um aeródromo. É reportado em intervalos regulares de uma hora.
#SPECI Informe meteorológico especial de aeródromo. Utilizado para a descrição completa das condições meteorológicas quando ocorrer uma ou mais variações significativas nas condições meteorológicas entre os intervalos das observações regulares.
#AUTO quando a abreviatura for inserida antes do grupo de vento, indicará que o informe foi gerado por uma EMS automática, sem intervenção humana.
#KT unidade de medida da velocidade de vento adotada pelo Brasil 
#G quando houver rajada de vento de velocidade média igual ou superior a 10KT, na coluna de vento à superfície aparecerá a letra G 
#V quando a variação total da direção do vento estiver entre 60º a 180º e a velocidade estiver 3kt ou maior serão informadas as duas direção e o V estará entre as duas
#RMK indica informações somente para uso exclusivo nacional
#visibilidade minima informa a direção em relação ao aerodromo 


import pandas as pd
import datetime as datetime
import json
import requests
import argparse
import csv
from flatten_json import flatten
from pprint import pprint


def dados_extraidos(station, yourkeyhere, date_initial, date_final):

    url = requests.get(f"https://api-redemet.decea.mil.br/mensagens/metar/{station}?api_key={yourkeyhere}&data_ini={date_initial}&data_fim={date_final}")
    clima = url.json()
    pprint(clima["data"]["data"])
    
    

    if isinstance(clima["data"]["data"], list):
        dict_flatten = (flatten(d) for d in clima["data"]["data"])
        df = pd.DataFrame(dict_flatten)
        df.to_csv(f"{station}.csv")  
        df.isnull().sum()
        

        try:
            clima["data"]["data"] == True
            print(clima)

        except ValueError as error:
            print(error)


def extract_column():

    extract = pd.read_csv(f"{station}.csv")
    extract[["Meteorological Code", "Station", "Time", "Wind Speed", "horizontal visibility", "visibilidade minima", "visual range", "present tense", "clouds", "air temperature", "atmospheric pressure"]] = (extract ["mens"].str.split(" ", expand=True))
    
    if 'COR' in extract["mens"]:
        print("Houve uma correção")
   
    if 'AUTO' in extract["mens"]:
        print("Gerado por uma EMS automática, sem intervenção humana")
    
    if 'CAVOK' or 'NSC' in extract["mens"]:
        print("Visibilidade 10km ou mais no horizonte, nenhuma nuvem ou evento metereologico significativo")
    
    if '00000KT' in extract["mens"]:
        print("Vento calmo, com velocidade inferior a 1kt")

    if 'VRB' in extract["mens"]:
        print("A variação total está entre 60 a 180 graus e sua velocidade media tem o valor inferior a 3kt ou sua direção for superior a 180 graus ou quando não for possivel determinar uma unica direção")
   
    if 'V' in extract["mens"]:
        print("A variação total está entre 60 a 180 graus e sua velocidade media tem o valor igual ou superior a 3kt")

#O valor da rajada aparecerá logo após a letra G

    if 'G' in extract["mens"]:
        print("Velocidade máxima do vento excedeu a velocidade média em 10kt ou mais")
   
    if 'P' in extract["mens"]:
        print("Quando o vento for igual ou maior que 100 kt")

#Visibilidade horizontal é expressa em metros
#quando houver mais de uma visibilidade minina, será informada a mais importante 

    if '9999' in extract["mens"]:
        print("Visibilidade igual ou superior a 10km")
        
def argumentos():
    
    description = "Choose the weather station and the state you want to get data from, example: SBBR(SB = Brasil, BR = Brasília), with capital letters. Soon after, inform your key obtained through the site https://www.atd-1.com/cadastro-api/, you will receive an email with the information. In the end add the initial and final date in YYYYMMDDHH format."
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("-s", "--stations", required = True)
    parser.add_argument("-k", "--key", required = True)
    parser.add_argument("-i", "--dateinitial", required = True)
    parser.add_argument("-f", "--datefinal", required = True)
    return parser.parse_args()  

if __name__ == "__main__":

    args = argumentos()
    station = args.stations
    yourkeyhere = args.key
    date_initial = args.dateinitial
    date_final = args.datefinal    
    dados_extraidos(station, yourkeyhere, date_initial, date_final)
    argumentos()
    extract_column()
   
    