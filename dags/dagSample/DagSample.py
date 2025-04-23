from datetime import datetime
from airflow import DAG
import requests
import pandas as pd
import os

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.decorators import task


dagName = "YourDagNameHere"

AIRFLOW_HOME = '/opt/airflow/clickboard'


with DAG(
    dag_id=f'{dagName}',  # Name of the DAG
    schedule_interval=None,  # Manual trigger
    catchup=False,  # No backfilling
    start_date=datetime(2021, 1, 1),
    tags=[f"{dagName}", "ETL Portfolio"]
) as dag:
    pass