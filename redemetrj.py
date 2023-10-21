import datetime as dt
import pandas as pd 
import requests
import json
import csv
import argparse


def qtd_stations():
    stations_rj = ['SBGL', 'SBAF', 'SBRJ', 'SBJR', 'SBSC']
    print("Na cidade do Rio de Janeiro temos o total de:", len(stations_rj), "estações metereológicas", (stations_rj))

def start_data(api_key, station, start_date, end_date, output_file):
    current_date = start_date
    dataframes = []
        
    while current_date <= end_date:
        url = requests.get(f"https://api-redemet.decea.mil.br/aerodromos/info?api_key={api_key}&localidade={station}&datahora={current_date}")
        clima = json.loads(url.text)
        
        if clima:
            df = pd.DataFrame(clima)

            df = df.drop("message", axis=1)
            df = df.drop("status", axis=1)
            dataset = df.T

            dataset.rename(columns={'ur': 'relative_humidity'}, inplace = True)
            dataset.rename(columns={'data': 'datatime'}, inplace = True)

            dataset['barometric_pressure'] = dataset['metar'].str.extract(r'(Q\d{4})')
            dataset['barometric_pressure'] = dataset['barometric_pressure'].str.replace('Q', '', regex=True)
            if 'vento' in dataset:
                dataset['wind_speed'] = dataset['vento'].str.extract(r'(\d{1,2}km/h)')
                dataset['wind_dir'] = dataset['vento'].str.extract(r'(\d{2,3}º)')
                dataset['wind_dir'] = dataset['wind_dir'].str.replace('º', '')
            else:
    
                dataset['wind_speed'] = None
                dataset['wind_dir'] = None
        
            dataset = dataset.drop("nome", axis=1)
            if 'ceu' in dataset:

                dataset = dataset.drop("ceu", axis=1)
        
            dataset = dataset.drop("cidade", axis=1)
            if 'condicoes_tempo' in dataset:

                dataset = dataset.drop("condicoes_tempo", axis=1)
            dataset = dataset.drop("localizacao", axis=1)
            dataset = dataset.drop("metar", axis=1)
            if 'tempoImagem' in dataset:

                dataset = dataset.drop("tempoImagem", axis=1)
            if 'teto' in dataset:

                dataset = dataset.drop("teto", axis=1)
            if 'visibilidade' in dataset:

                dataset = dataset.drop("visibilidade", axis=1)
            if 'vento' in dataset:
                dataset = dataset.drop("vento", axis=1)
            dataset = dataset.drop("lat", axis=1)
            dataset = dataset.drop("lon", axis=1)

            dataframes.append(dataset)
            
        current_date = (dt.datetime.strptime(current_date, "%Y%m%d%H") + dt.timedelta(hours=1)).strftime("%Y%m%d%H")
           
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df.to_csv(f"{output_file}.csv", index=False)
        print(f'Dados salvos em {output_file}.csv')


def argumentos():
    description = "Escolha a estação meteorológica, sua chave de API e as datas de início e fim no formato AAAAMMDDHH."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-k", "--key", required=True, help="Chave de API")
    parser.add_argument("-s", "--station", required=True, help="Estação meteorológica (exemplo: SBBR)")
    parser.add_argument("-start", "--start_date", required=True, help="Data de início no formato AAAAMMDDHH")
    parser.add_argument("-end", "--end_date", required=True, help="Data de fim no formato AAAAMMDDHH")
    parser.add_argument("-o", "--output_file", required=True, help="Nome do arquivo de saída CSV")
    return parser.parse_args()

if __name__ == "__main__":
    qtd_stations()
    args = argumentos()
    start_data(args.key, args.station, args.start_date, args.end_date, args.output_file)
    