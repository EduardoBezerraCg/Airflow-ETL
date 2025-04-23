from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def _task2():
    print("this is task2")


with DAG(
    dag_id="My_Second_Dag",
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False
) as dag:

    task1 = BashOperator(
        task_id="task1",
        bash_command="echo 'this istask1'",
    )

    task2 = PythonOperator(
        task_id="task2",
        python_callable=_task2,
    )

    task1 >> task2