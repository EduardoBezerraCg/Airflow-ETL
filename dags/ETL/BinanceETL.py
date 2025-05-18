from datetime import datetime
from airflow import DAG
import requests
import pandas as pd
import os

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.decorators import task


dagName = "BinanceCryptoAPI"

AIRFLOW_HOME = '/opt/airflow/clickboard'


def connect_to_db():
    try:
        pg_hook = PostgresHook(postgres_conn_id="DBPostgres")
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        print("Connection to database successful")

        sqlQuery = """SELECT * FROM cryptoInfo"""

        pg_hook.run(sqlQuery)
        
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        raise

def extract_crypto_data():
    url = "https://api4.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()
    df= pd.DataFrame(data)
    print(df.head())

    #Check if already exists
    if os.path.exists(f"{AIRFLOW_HOME}/cryptoInfo.csv"):
        os.remove(f"{AIRFLOW_HOME}/cryptoInfo.csv")
    renderer = df.to_csv(f"{AIRFLOW_HOME}/cryptoInfo.csv", index=False)


    return renderer

def transfor_crypto_data():
    df =pd.read_csv(f"{AIRFLOW_HOME}/cryptoInfo.csv")
    #Selecting only required columns
    selected_df = df[['symbol', 'priceChange', 'priceChangePercent', 'lastPrice', 'volume', 'quoteVolume']]

    selected_df.to_csv(f"{AIRFLOW_HOME}/cryptoInfo_transformed.csv", index=False)

    print(selected_df.head())
    


def create_insert_sql():

    df = pd.read_csv(f"{AIRFLOW_HOME}/cryptoInfo_transformed.csv")
    file_string = ''

    for index, row in df.iterrows():
        file_string += (
            f"INSERT INTO cryptoInfo "
            f"(symbol, priceChange, priceChangePercent, lastPrice, volume, quoteVolume) "
            f"VALUES ('{row['symbol']}', '{row['priceChange']}', '{row['priceChangePercent']}', "
            f"'{row['lastPrice']}', '{row['volume']}', '{row['quoteVolume']}');\n"
        )

    with open(f"{AIRFLOW_HOME}/insert_crypto.sql", 'w') as f:
        f.write(file_string)

@task
def load_crypto_data():
    pg_hook = PostgresHook(postgres_conn_id="DBPostgres")

    with open(f"{AIRFLOW_HOME}/insert_crypto.sql", 'r') as f:
        sql_script = f.read()

    pg_hook.run(sql_script)
    print("Dados inseridos com sucesso via script SQL.")



with DAG(
    dag_id=f'{dagName}',  # Name of the DAG
    schedule_interval=None,  # Manual trigger
    catchup=False,  # No backfilling
    start_date=datetime(2021, 1, 1),
    tags=[f"{dagName}", "ETL Portfolio"]
) as dag:
    TestConDB = PythonOperator(
        task_id='TestConnectionDB',
        python_callable=connect_to_db
    )

    ExtractCryptoData = PythonOperator(
        task_id='ExtractCryptoData',
        python_callable=extract_crypto_data
    )
    TransforCryptoData = PythonOperator(
        task_id='transfor_crypto_data',
        python_callable=transfor_crypto_data
    )

    CreateInsertSQL = PythonOperator(
        task_id='create_insert_sql',
        python_callable=create_insert_sql
    )

    # LoadCryptoData = PythonOperator(
    #     task_id='load_crypto_data',
    #     python_callable=load_crypto_data
    # )

    TestConDB >> [ExtractCryptoData, TransforCryptoData, CreateInsertSQL] >> load_crypto_data()