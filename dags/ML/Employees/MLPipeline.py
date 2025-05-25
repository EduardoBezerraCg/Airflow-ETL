from datetime import datetime
from airflow import DAG
import requests
import pandas as pd
import os
import sys

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.decorators import task


dagName = "MlPipeline Employees"

AIRFLOW_HOME_OUTPUT = '/opt/airflow/clickboard'

HOME = '/opt/airflow/dags/ML/Employees'
sys.path.append(f'{HOME}/Pipeline')



with DAG(
    dag_id=f'{dagName}',  # Name of the DAG
    schedule_interval=None,  # Manual trigger
    catchup=False,  # No backfilling
    start_date=datetime(2021, 1, 1),
    tags=[f"{dagName}", "ETL Portfolio"]
) as dag:
    
    @task
    def init_task():
        os.mkdir


    @task
    def load_training_data():
        pass

    @task
    def preprocess_data():
        pass

    @task
    def split_data():
        pass

    @task
    def training_task():
        pass

    @task
    def save_model():
        pass

    @task
    def evaluate_model():
        pass

    init_task() >> load_training_data() >> preprocess_data() >> split_data() >> training_task() >> save_model() >> evaluate_model