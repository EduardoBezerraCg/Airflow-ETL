import os
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime



# Function to write data from the DB to CSV (Task 1)
def write_data_to_csv(**kwargs):
    # Create a PostgresHook to connect to the database
    pg_hook = PostgresHook(postgres_conn_id="Con_MyDb")  # Ensure you have this connection defined in Airflow

    # SQL Query to fetch data (for example, fetching all records from a table 'employees')
    sql = "SELECT * FROM employees;"

    # Fetch records using pandas directly
    df = pg_hook.get_pandas_df(sql)

    # If records are retrieved, proceed to write to CSV
    if not df.empty:
        # Define the clickboard folder path
        clickboard_dir = "/DataExports"  # Replace with your actual clickboard path
        
        # Ensure the directory exists
        if not os.path.exists(clickboard_dir):
            os.makedirs(clickboard_dir)
            print(f"Created directory: {clickboard_dir}")

        # File path to save the CSV in the clickboard folder
        file_path = os.path.join(clickboard_dir, "employees_data.csv")
        
        # Write the DataFrame to a CSV file
        df.to_csv(file_path, index=False)

        print(f"Data has been written to {file_path}")
        return "Data written successfully"
    else:
        raise ValueError("No data fetched from the database")

# Dummy task (Task 2)
def dummy_task(**kwargs):
    print("Dummy task executed.")
    return "Dummy task completed."

# Define the Airflow DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 9),  # Adjust the start date as needed
    'retries': 1,
}

# Use the context manager `with DAG as dag` for defining the DAG
with DAG(
    'My_Fourth_Dag',  # Name of the DAG
    default_args=default_args,
    schedule_interval=None,  # Manual trigger
    catchup=False,  # No backfilling
) as dag:

    # Task 1: Get data from DB and write to CSV
    task1 = PythonOperator(
        task_id='write_db_data_to_csv',  # Task name
        python_callable=write_data_to_csv,  # Function to call
        provide_context=True,  # Allows you to access the context (kwargs)
    )

    # Task 2: Execute a dummy task
    task2 = PythonOperator(
        task_id='dummy_task',  # Task name
        python_callable=dummy_task,  # Function to call
        provide_context=True,  # Allows you to access the context (kwargs)
    )

    # Define task dependencies (task1 -> task2)
    task1 >> task2  # task2 will execute after task1 finishes