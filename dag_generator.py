import json
import importlib
from airflow import DAG
from airflow.utils.dates import days_ago
import os
import sys

# Add the plugins directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'plugins'))


# Importing custom operator module
def load_operator(module_name, operator_name):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, operator_name)
    except ImportError as e:
        raise ImportError(f"Error importing module {module_name}: {e}")
    except AttributeError as e:
        raise AttributeError(f"Module {module_name} has no attribute {operator_name}: {e}")

def generate_dag_file(json_input_data, output_dir):
    with open(json_input_data, 'r') as file:
        config = json.load(file)

    dag_params = config['dag_params']
    tasks = config['tasks']
    dependencies = config['dependencies']

    # DAG template
    # Indentation to the left is necessary. DO NOT CHANGE THE FORMAT
    dag_file_content = f"""
from airflow import DAG
from airflow.utils.dates import days_ago

default_args = {{
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}}

dag = DAG(
    dag_id='{dag_params['dag_id']}',
    default_args=default_args,
    description='A dynamically generated DAG',
    schedule_interval='{dag_params['schedule_interval']}',
    start_date=days_ago(1)
)

task_dict = {{}}

                        """

    # Generate task definitions
    for task in tasks:
        task_id = task['task_id']
        operator = task['operator']
        params = task['params']
        
        # Convert params to kwargs format
        params_str = ', '.join([f"{key}='{value}'" for key, value in params.items()])

        operator_class = load_operator(f"plugins.{operator.lower()}", operator)
        
        # Generate tasks for dag
        # Indentation to the left is necessary. DO NOT CHANGE THE FORMAT
        dag_file_content += f"""
task_dict['{task_id}'] = {operator_class}(task_id='{task_id}', {params_str}, dag=dag)
                            """

    # Generate task dependencies
    for dependency in dependencies:
        upstream_task_id, downstream_task_id = dependency

        # Indentation to the left is necessary. DO NOT CHANGE THE FORMAT
        dag_file_content += f"""
task_dict['{upstream_task_id}'] >> task_dict['{downstream_task_id}']
                            """

    # Write the generated content to a Python file
    dag_file_name = os.path.join(output_dir, f"{dag_params['dag_id']}.py")
    with open(dag_file_name, 'w') as f:
        f.write(dag_file_content)
    print(f"DAG file created: {dag_file_name}")


# Path to your JSON configuration file
    
# Directory of the current script directory
script_directory = os.path.dirname(os.path.abspath(__file__)) # for relative path use os.path.relpath 

# Path to the file
json_input_data = os.path.join(script_directory, 'config/config.json') # This will change to pick up json_input during runtime
output_dir = os.path.join(script_directory, 'dags/')

# Generate the DAG file dynamically
generate_dag_file(json_input_data, output_dir)
