from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import pandas as pd
import os
import sys

# Append scripts path to import our custom data quality functions directly in Airflow
sys.path.insert(0, '/opt/airflow/scripts')
from data_quality_checks import check_sales_data, check_inventory_data

default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='2_ecom_transformation_pipeline',
    default_args=default_args,
    description='Transforms and Validates Raw E-commerce Data',
    schedule_interval='0 3 * * *', # Runs at 3:00 AM (After ingestion)
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['transformation', 'sensor', 'dq'],
) as dag:

    # 1. Start Node
    start_transform = EmptyOperator(task_id='start_transform')

    # Path Configuration (Jinja templated based on execution date)
    RAW_PATH = "/opt/airflow/data/raw/{{ ds }}"
    PROCESSED_PATH = "/opt/airflow/data/processed/{{ ds }}"

    # 2. File Sensors (Wait for upstream files to exist before processing)
    with TaskGroup("wait_for_raw_data") as wait_for_data:
        wait_for_sales = FileSensor(
            task_id='wait_for_sales_csv',
            filepath=RAW_PATH + '/sales.csv',
            timeout=60 * 30, # Max 30 minutes waiting
            mode='poke',
            poke_interval=60
        )
        
        wait_for_inventory = FileSensor(
            task_id='wait_for_inventory_csv',
            filepath=RAW_PATH + '/inventory.csv',
            timeout=60 * 30,
            mode='poke',
            poke_interval=60
        )

    # Note: Python functions must be defined to be passed to PythonOperator
    def clean_sales(execution_date):
        raw_file = f"/opt/airflow/data/raw/{execution_date}/sales.csv"
        proc_dir = f"/opt/airflow/data/processed/{execution_date}"
        os.makedirs(proc_dir, exist_ok=True)
        
        df = pd.read_csv(raw_file)
        # Simple Transformation: Standardize status and create net_amount
        df['status'] = df['status'].str.upper()
        df['net_amount'] = df['amount'] * 0.95 # Deduct generic 5% fees
        output_file = f"{proc_dir}/clean_sales.csv"
        df.to_csv(output_file, index=False)
        return output_file # Pushes to XCom

    def clean_inventory(execution_date):
        raw_file = f"/opt/airflow/data/raw/{execution_date}/inventory.csv"
        proc_dir = f"/opt/airflow/data/processed/{execution_date}"
        os.makedirs(proc_dir, exist_ok=True)

        df = pd.read_csv(raw_file)
        # Transformation: Flag Low Stock
        df['is_low_stock'] = df['stock_level'] < 50
        output_file = f"{proc_dir}/clean_inventory.csv"
        df.to_csv(output_file, index=False)
        return output_file # Pushes to XCom


    # 3. Transform & Validate TaskGroups
    with TaskGroup("process_sales_data") as process_sales:
        clean_sales_task = PythonOperator(
            task_id='clean_sales',
            python_callable=clean_sales,
            op_kwargs={'execution_date': '{{ ds }}'}
        )
        
        dq_check_sales_task = PythonOperator(
            task_id='quality_check_sales',
            python_callable=check_sales_data,
            op_kwargs={'filepath': PROCESSED_PATH + '/clean_sales.csv'}
        )
        clean_sales_task >> dq_check_sales_task


    with TaskGroup("process_inventory_data") as process_inventory:
        clean_inventory_task = PythonOperator(
            task_id='clean_inventory',
            python_callable=clean_inventory,
            op_kwargs={'execution_date': '{{ ds }}'}
        )
        
        dq_check_inventory_task = PythonOperator(
            task_id='quality_check_inventory',
            python_callable=check_inventory_data,
            op_kwargs={'filepath': PROCESSED_PATH + '/clean_inventory.csv'}
        )
        clean_inventory_task >> dq_check_inventory_task

    # 4. End Node
    end_transform = EmptyOperator(task_id='end_transform')

    # Define DAG Dependencies
    start_transform >> wait_for_data
    wait_for_data >> process_sales >> end_transform
    wait_for_data >> process_inventory >> end_transform
