
from airflow import DAG
from airflow.utils.dates import days_ago
from custom_operators.postgresoperatortemplate import *  # Need to make this dynamic


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    dag_id='dynamic_dag_generation_test',
    default_args=default_args,
    description='A dynamically generated DAG',
    schedule_interval='@daily',
    start_date=days_ago(1)
)

task_dict = {}

                        
task_dict['source'] = PostgresOperatorTemplate(task_id='source', postgres_conn_id='postgres_conn', sql='SELECT 1', dag=dag)
                            
task_dict['transform'] = PostgresOperatorTemplate(task_id='transform', postgres_conn_id='postgres_conn', sql='SELECT 2', dag=dag)
                            
task_dict['destination'] = PostgresOperatorTemplate(task_id='destination', postgres_conn_id='postgres_conn', sql='SELECT 3', dag=dag)
                            
task_dict['source'] >> task_dict['transform']
                            
task_dict['transform'] >> task_dict['destination']
                            