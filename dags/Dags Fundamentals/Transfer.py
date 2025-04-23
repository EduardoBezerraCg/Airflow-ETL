from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import pandas as pd

dbConnection = "Con_MyDb"

def transfer_data():
    """
    Transfere dados da tabela 'employees' para a tabela 'employee_copy'.
    """
    source_hook = PostgresHook(postgres_conn_id=dbConnection)
    
    # Obtém os dados da tabela 'employees'
    source_data = source_hook.get_pandas_df("SELECT * FROM employees")
    
    if not source_data.empty:
        dest_hook = PostgresHook(postgres_conn_id=dbConnection)
        engine = dest_hook.get_sqlalchemy_engine()
        
        # Insere os dados na tabela 'employee_copy'
        source_data.to_sql(
            'employee_copy',  # Nome da tabela de destino
            engine,
            if_exists='append',  # Adiciona os dados (não substitui)
            index=False          # Não insere o índice do DataFrame como coluna
        )
        print(f"Transferidos {len(source_data)} registros para a tabela 'employee_copy'.")
    else:
        print("Nenhum dado encontrado para transferir.")

def check_data_with_pandas():
    """
    Verifica os dados na tabela 'employee_copy' e imprime o head usando pandas.
    """
    hook = PostgresHook(postgres_conn_id=dbConnection)
    
    # Obtém os dados da tabela 'employee_copy' como DataFrame pandas
    df = hook.get_pandas_df("SELECT * FROM employee_copy;")
    
    if not df.empty:
        print("Dados na tabela 'employee_copy':")
        print(df.head())
    else:
        print("A tabela 'employee_copy' está vazia.")

# Definição do DAG
with DAG(
    dag_id='Transfer_Data_Dag_SQLExecuteQuery',
    schedule_interval=None,
    catchup=False,
    start_date=datetime(2021, 1, 1),
    tags=["Transfer Data"],
) as dag:

    # Tarefa para criar a tabela usando SQLExecuteQueryOperator
    create_table_task = SQLExecuteQueryOperator(
        task_id='CreateTable',
        conn_id=dbConnection,
        sql="""
        CREATE TABLE IF NOT EXISTS employee_copy (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            department VARCHAR(50) NOT NULL,
            salary NUMERIC NOT NULL
        )
        """
    )

    # Tarefa para transferir os dados com PythonOperator (mantida)
    transfer_task = PythonOperator(
        task_id='TransferData',
        python_callable=transfer_data
    )

    # Tarefa para verificar os dados com PythonOperator usando pandas
    check_task = PythonOperator(
        task_id='CheckDataWithPandas',
        python_callable=check_data_with_pandas
    )

# Definindo a ordem das tarefas no DAG
create_table_task >> transfer_task >> check_task
