from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'retries': 0, # Usually reporting queries can be non-retriable or idempotent
}

def determine_reporting_path(execution_date):
    """
    Branch logic: Returns the task_id of the next task to execute based on the day of week.
    """
    date_obj = datetime.strptime(execution_date, '%Y-%m-%d')
    day_of_week = date_obj.weekday()
    
    # 5 = Saturday, 6 = Sunday
    if day_of_week >= 5:
        print("➡️ Selected Path: Weekend Report")
        return 'generate_weekend_report'
    else:
        print("➡️ Selected Path: Weekday Report")
        return 'generate_weekday_report'

def mock_dwh_load(execution_date, path):
    print(f"✅ Loaded final {path} aggregation for {execution_date} to PostgreSQL DWH")
    return "SUCCESS"

with DAG(
    dag_id='3_ecom_reporting_pipeline',
    default_args=default_args,
    description='Generates business impact reports depending on the day of week',
    schedule_interval='0 6 * * *', # Runs at 6:00 AM
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['reporting', 'branching', 'dwh'],
) as dag:

    # 1. Start Node
    start_reporting = DummyOperator(task_id='start_reporting')

    # 2. Branch Decision
    branch_task = BranchPythonOperator(
        task_id='decide_report_type',
        python_callable=determine_reporting_path,
        op_kwargs={'execution_date': '{{ ds }}'}
    )

    # 3. Path A: Weekday Reporting
    weekday_report = PythonOperator(
        task_id='generate_weekday_report',
        python_callable=mock_dwh_load,
        op_kwargs={'execution_date': '{{ ds }}', 'path': 'WEEKDAY'}
    )

    # 4. Path B: Weekend Reporting
    weekend_report = PythonOperator(
        task_id='generate_weekend_report',
        python_callable=mock_dwh_load,
        op_kwargs={'execution_date': '{{ ds }}', 'path': 'WEEKEND'}
    )

    # 5. Join Node (Requires TriggerRule because one of the upstream paths will be Skipped)
    join_reports = DummyOperator(
        task_id='join_reports',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    # 6. Final Notification (Send Slack/Email alert concept)
    notify_success = DummyOperator(
        task_id='send_success_notification'
    )

    # Define DAG Dependencies
    start_reporting >> branch_task
    branch_task >> weekday_report >> join_reports
    branch_task >> weekend_report >> join_reports
    join_reports >> notify_success
