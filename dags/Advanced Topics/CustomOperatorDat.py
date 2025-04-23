from datetime import datetime
from airflow import DAG

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.decorators import task
#from Mask_CSV_Operator import MarkCSVOperator

import pandas as pd

AIRFLOW_HOME = '/opt/airflow/clickboard'

def read_fs():
    df = pd.read_csv(f"{AIRFLOW_HOME}/store_transactions.csv")
    print(df.head())

def create_user():
    # Create a PostgresHook to connect to the database
    pg_hook = PostgresHook(postgres_conn_id="Con_MyDb")  # Ensure you have this connection defined in Airflow

    # SQL Query to create a new user
    sql = """
    CREATE USER airflowreserve WITH PASSWORD 'airflowserve';
    """

    # Execute the query
    pg_hook.run(sql)

with DAG(
    dag_id='Dag_CustomOperator',  # Name of the DAG
    schedule_interval=None,  # Manual trigger
    catchup=False,  # No backfilling
    start_date=datetime(2021, 1, 1),
    tags=["Dag_CustomOperator", "Experiment"]
) as dag:
    readHeadFile = PythonOperator(
        task_id='read_file',
        python_callable=read_fs
    )

    createUserTask = PythonOperator(
        task_id='create_user',
        python_callable=create_user
    )

    readHeadFile >> createUserTask
