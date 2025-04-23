from datetime import datetime
from airflow import DAG

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import pandas as pd

AIRFLOW_HOME = '/opt/airflow/clickboard'

def read_fs():
    df = pd.read_csv(f"{AIRFLOW_HOME}/store_transactions.csv")
    print(df.head())

def read_sql():
    # Create a PostgresHook to connect to the database
    pg_hook = PostgresHook(postgres_conn_id="Con_MyDb")  # Ensure you have this connection defined in Airflow

    # SQL Query to fetch data (for example, fetching all records from a table 'employees')
    sql = "SELECT * FROM employees;"

    # Fetch records using pandas directly
    df = pg_hook.get_pandas_df(sql)

with DAG(
    dag_id='Load',  # Name of the DAG
    schedule_interval=None,  # Manual trigger
    catchup=False,  # No backfilling
    start_date=datetime(2021, 1, 1),
    #end_date=datetime(2022, 1, 1),
    tags=["Load","Experiment"]
) as dag:
    task1 = PythonOperator(
        task_id='read_file',  
        python_callable=read_fs,  
        provide_context=True,  
    )
    task2 = PythonOperator(
        task_id='read_sql',  
        python_callable=read_sql,  
        provide_context=True,  
    )
    
    