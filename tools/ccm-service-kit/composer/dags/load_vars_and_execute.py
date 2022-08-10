
from datetime import datetime, timedelta
from airflow.contrib.operators import bigquery_operator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
# The DAG object we'll need this to instantiate a DAG
from airflow import DAG
from airflow.models import Variable
import os


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Define DAG: Set ID and assign default args, tags and schedule variables.
with DAG(
    'load_vars_and_execute',
    default_args=default_args,
    description='Load variables and execute DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    is_paused_upon_creation = True,
    tags=['ccm-model'],
) as dag:

    copy_variables_file = BashOperator(
        task_id="copy_variables_file",
        dag=dag,
        bash_command='gsutil cp gs://us-central1-tftest1-64bc2b2a-bucket/variables.json ${AIRFLOW_HOME}/variables.json',
    )

    airflow_command = BashOperator(
        task_id="airflow_command",
        dag=dag,
        bash_command='airflow variables import ${AIRFLOW_HOME}/variables.json',
    )

#TODO: After loading the variables, execute the DAG

copy_variables_file >> airflow_command