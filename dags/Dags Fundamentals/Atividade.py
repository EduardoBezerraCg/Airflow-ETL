from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule

from datetime import timedelta
import random

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def print_mensagem():
    print("Olá, esta é uma task Python!")

def extrair_valor():
    return random.choice(['caminho_a', 'caminho_b'])

def usar_postgres():
    hook = PostgresHook(postgres_conn_id='Con_MyDb')
    result = hook.get_first("SELECT NOW();")
    print(f"Data e hora atual no banco: {result[0]}")

with DAG(
    dag_id='dag_complexa_exemplo',
    default_args=default_args,
    description='Module_Dags',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['exemplo', 'complexo']
) as dag:

    task_python = PythonOperator(
        task_id='task_python',
        python_callable=print_mensagem
    )

    task_bash = BashOperator(
        task_id='listar_arquivos',
        bash_command='ls -l'
    )

    task_postgres = PythonOperator(
        task_id='consultar_postgres',
        python_callable=usar_postgres
    )

    escolher_caminho = BranchPythonOperator(
        task_id='escolher_caminho',
        python_callable=extrair_valor
    )

    caminho_a = BashOperator(
        task_id='caminho_a',
        bash_command='echo "Executando o caminho A"'
    )

    caminho_b = BashOperator(
        task_id='caminho_b',
        bash_command='echo "Executando o caminho B"'
    )

    fim = BashOperator(
        task_id='fim',
        bash_command='echo "Fim do fluxo!"',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    # Definindo o fluxo da DAG
    [task_python, task_bash] >> task_postgres >> escolher_caminho
    escolher_caminho >> [caminho_a, caminho_b] >> fim
