#Cada solicitação permite buscar o equivalente a 8.760 registros aproximadamente.
#Há disponibilidade de mensagens desde 01/01/2003 até a presente data.

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