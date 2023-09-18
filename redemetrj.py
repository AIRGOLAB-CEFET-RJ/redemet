#descobrir quando cada estação começou a operar OK
#qtd de estações na cidade do RJ  OK
#variaveis e unidade de medida OK
#resolução temporal - ATRAVÉS DO OUTRO SCRIPT, COLUNA RECEBIMENTO, menor tempo 15 min 
#periodo de operação de cada estação OK
#latitude e longitude de cada estação OK

#eliminar a coluna vazia message OK
#transformar dados da coluna data em coluna OK

#pegar o valor da pressao OK
# pegar o valor da velocidade em km do vento OK
#pegar o valor do grau no campo vento OK
#datetime valor da data OK
#relative_humidity valor do campo ur OK
#fazer um looping pro usuario colocar data inicial e final e obter os dados de 24h dessas datas


import datetime as datetime
import pandas as pd 
import numpy as np
import math
import chardet
import time
import requests
import json
import csv
import argparse
import re


def qtd_stations():

    stations_rj = ['SBGL', 'SBAF', 'SBRJ', 'SBJR', 'SBSC']
    print("Na cidade do Rio de Janeiro temos o total de:", len(stations_rj), "estações metereológicas", (stations_rj))



def start_data(api_key, station, date):

    url = requests.get(f"https://api-redemet.decea.mil.br/aerodromos/info?api_key={api_key}&localidade={station}&datahora={date}")
    clima = json.loads(url.text)
    df = pd.DataFrame(clima)
    df = df.drop("message", axis = 1)
    df = df.drop("status", axis = 1)
    dataset = df.T
    dataset['barometric_pressure'] = dataset['metar'].str.extract(r'(Q\d{4})')
    dataset['wind_speed'] = dataset['vento'].str.extract(r'(\d{2}km/h)')
    dataset['wind_dir'] = dataset['vento'].str.extract(r'(\d{3}º)')
    dataset.to_csv(f"{station}.csv", index=False)
    print(dataset)
 
    
def argumentos():
    
    description = "Choose the weather station and the state you want to get data from, example: SBBR(SB = Brasil, BR = Brasília), with capital letters. Soon after, inform your key obtained through the site https://www.atd-1.com/cadastro-api/, you will receive an email with the information. In the end add the initial and final date in YYYYMMDDHH format."
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("-k", "--key", required = True)
    parser.add_argument("-s", "--stations", required = True)
    parser.add_argument("-e", "--data", required = True)
    return parser.parse_args()  

if __name__ == "__main__":

    est_met = qtd_stations()
    args = argumentos()
    yourkeyhere = args.key
    station = args.stations
    date = args.data
    start_data(yourkeyhere, station, date)
    argumentos()
    
    
    
    