import pandas as pd
import argparse

def conc(output_file):
    dataframes = []


    for i in range(1, 7):
        nome_arquivo = input(f"Digite o nome do arquivo CSV {i}: ")
        
        try:
            
            df = pd.read_csv(nome_arquivo)
            dataframes.append(df)
        except FileNotFoundError:
            print(f"O arquivo {nome_arquivo} não foi encontrado.")
        except Exception as e:
            print("Ocorreu um erro:", e)


    merged_data = pd.concat(dataframes, ignore_index=True)

    try:
    
        merged_data.to_parquet(f'{output_file}.parquet')
        print("Os arquivos foram concatenados e salvos como Parquet com sucesso.")
    except Exception as e:
        print("Ocorreu um erro ao salvar como Parquet:", e)

def argumentos():
    description = "Dar um nome pro novo formato"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-o", "--output_file", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = argumentos()
    conc(args.output_file)