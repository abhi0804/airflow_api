
from airflow import DAG
from airflow.utils.dates import days_ago

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

                        
task_dict['fetch_data'] = <class 'plugins.postgresoperatortemplate.PostgresOperatorTemplate'>(task_id='fetch_data', postgres_conn_id='postgres_conn', sql='SELECT 1', dag=dag)
                            
task_dict['process_data'] = <class 'plugins.postgresoperatortemplate.PostgresOperatorTemplate'>(task_id='process_data', postgres_conn_id='postgres_conn', sql='SELECT 2', dag=dag)
                            
task_dict['store_data'] = <class 'plugins.postgresoperatortemplate.PostgresOperatorTemplate'>(task_id='store_data', postgres_conn_id='postgres_conn', sql='SELECT 3', dag=dag)
                            
task_dict['fetch_data'] >> task_dict['process_data']
                            
task_dict['process_data'] >> task_dict['store_data']
                            