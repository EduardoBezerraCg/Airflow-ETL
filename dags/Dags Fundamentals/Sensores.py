import pandas as pd
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sensors.filesystem import FileSensor
from datetime import datetime

#--->Your functions goes here<-----#

def read_file():
    for path in os.listdir('/DataExports'):
        print(path)


with DAG(
    dag_id='Sensor_dag',  # Name of the DAG
    schedule_interval=None,  # Manual trigger
    catchup=False,  # No backfillingf
    start_date=datetime(2021, 1, 1),
    #end_date=datetime(2022, 1, 1),
    tags=["DagScheduler","Experiment"]
) as dag:

    # Task 1: Get data from DB and write to CSV
    sensor = FileSensor(
        task_id='filesensor',  # Task name
        filepath='/DataExports',  # Function to call
        fs_conn_id='FS_CONN',
        poke_interval=5
    )

    # Task 2: Execute a dummy task
    readFile = PythonOperator(
        task_id='read_file',  # Task name
        python_callable= read_file,  # Function to call
        provide_context=True,  # Allows you to access the context (kwargs)
    )

    # Define task dependencies (task1 -> task2)
    sensor >> readFile  # task2 will execute after task1 finishes