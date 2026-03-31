from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import os

# Define Default Arguments for robust production execution
default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3, # Advanced: Retries gracefully instead of failing immediately
    'retry_delay': timedelta(minutes=1),
    'execution_timeout': timedelta(minutes=10) # Fails if running too long
}

with DAG(
    dag_id='1_ecom_ingestion_pipeline',
    default_args=default_args,
    description='Extracts daily sales and inventory data from mock APIs',
    schedule_interval='0 2 * * *',  # Runs daily at 2:00 AM
    start_date=datetime(2025, 1, 1),
    catchup=False, # Demonstrating Catchup control
    tags=['ingestion', 'ecom'],
) as dag:

    # 1. Start Node
    start_ingestion = EmptyOperator(task_id='start_ingestion')

    # Data Paths
    RAW_DATA_PATH = "/opt/airflow/data/raw/{{ ds }}"
    SCRIPT_PATH = "/opt/airflow/scripts/mock_api_extractor.py"
    
    # 2. Extract Sales Data
    # Parallel Task 1
    extract_sales = BashOperator(
        task_id='extract_sales_data',
        bash_command=f"python {SCRIPT_PATH} --date {{{{ ds }}}} --type sales --output {RAW_DATA_PATH}/sales.csv",
    )

    # 3. Extract Inventory Data
    # Parallel Task 2
    extract_inventory = BashOperator(
        task_id='extract_inventory_data',
        bash_command=f"python {SCRIPT_PATH} --date {{{{ ds }}}} --type inventory --output {RAW_DATA_PATH}/inventory.csv",
    )

    # 4. End Node
    end_ingestion = EmptyOperator(task_id='end_ingestion')

    # Define Dependencies (Sequential & Parallel)
    start_ingestion >> [extract_sales, extract_inventory] >> end_ingestion
