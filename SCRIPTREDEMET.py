import pandas as pd
import datetime as datetime
import json
import requests
import argparse
from flatten_json import flatten
from pprint import pprint



def dados_extraidos(data_inicial, data_final):
    url = requests.get(f"https://api-redemet.decea.mil.br/mensagens/metar/SBGL,SBBR?api_key=Cz1Rhi3nf2sBSUjMWXELLrbApsoNTo0bhlmLKps9&data_ini={data_inicial}&data_fim={data_final}")
    clima = url.json()
    pprint(clima["data"]["data"])
    
    if isinstance(clima["data"]["data"], list):
        dict_flatten = (flatten(d) for d in clima["data"]["data"])
        df = pd.DataFrame(dict_flatten)
        df.to_csv("DadosRedeMet.csv")
        
        
def argumentos():
    
    description = "Formato da data YYYYMMDDHH"
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("-i", "--datainicial")
    parser.add_argument("-f", "--datafinal")
    return parser.parse_args()  
    
if __name__ == '__main__':
    
    args = argumentos()
    data_inicial = args.datainicial
    data_final = args.datafinal

    dados_extraidos(data_inicial, data_final)