
from airflow import DAG
from airflow.utils.dates import days_ago                        


from custom_operators.extractoperator import ExtractOperator      


from custom_operators.transformoperator import TransformOperator      


from custom_operators.loadoperator import LoadOperator      




from custom_operators.extractoperator import ExtractOperator      


from custom_operators.transformoperator import TransformOperator      


from custom_operators.loadoperator import LoadOperator      


     


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'example_dynamic_dag_with_custom_operators_test2',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)



job_1_extract_data = ExtractOperator(
    task_id='job_1_extract_data',
    dag=dag,
    **{'conn_id': 'postgres_default', 'sql': 'SELECT * FROM table1', 'output_path': '/tmp/job1_extracted_data.parquet'}
)

job_1_transform_data = TransformOperator(
    task_id='job_1_transform_data',
    dag=dag,
    **{'input_path': '/tmp/job1_extracted_data.parquet', 'output_path': '/tmp/job1_transformed_data.parquet', 'transformations': {'column1': 'str_to_int', 'column2': 'float_to_str'}}
)

job_1_load_to_s3 = LoadOperator(
    task_id='job_1_load_to_s3',
    dag=dag,
    **{'input_path': '/tmp/job1_transformed_data.parquet', 's3_bucket': 'bucket1', 's3_key': 'job1/path/to/data.parquet'}
)



job_2_extract_data = ExtractOperator(
    task_id='job_2_extract_data',
    dag=dag,
    **{'conn_id': 'postgres_default', 'sql': 'SELECT * FROM table2', 'output_path': '/tmp/job2_extracted_data.parquet'}
)

job_2_transform_data = TransformOperator(
    task_id='job_2_transform_data',
    dag=dag,
    **{'input_path': '/tmp/job2_extracted_data.parquet', 'output_path': '/tmp/job2_transformed_data.parquet', 'transformations': {'column1': 'str_to_int', 'column2': 'float_to_str'}}
)

job_2_load_to_s3 = LoadOperator(
    task_id='job_2_load_to_s3',
    dag=dag,
    **{'input_path': '/tmp/job2_transformed_data.parquet', 's3_bucket': 'bucket2', 's3_key': 'job2/path/to/data.parquet'}
)



# Set task and job dependencies





job_1_extract_data >> job_1_transform_data



job_1_transform_data >> job_1_load_to_s3







job_2_extract_data >> job_2_transform_data



job_2_transform_data >> job_2_load_to_s3








job_1_load_to_s3 >> job_2_extract_data



                        