import json
from airflow.utils.dates import days_ago
import os
import sys
from jinja2 import Template

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_dag_file(config):

    # DAG template
    # Indentation to the left is necessary. DO NOT CHANGE THE FORMAT
    template = Template("""
from airflow import DAG
from airflow.utils.dates import days_ago                        
{% for job in jobs %}
{% for task in job.tasks %}
from custom_operators.{{task.operator.lower()}} import {{ task.operator }}      

{% endfor %}
{% endfor %}     


default_args = {
    'owner': '{{ default_args.owner }}',
    'start_date': days_ago(1),
    'retries': {{ default_args.retries }},
}

dag = DAG(
    '{{ dag_id }}',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

{% for job in jobs %}
{% for task in job.tasks %}
{{ job.job_id }}_{{ task.task_id }} = {{ task.operator }}(
    task_id='{{ job.job_id }}_{{ task.task_id }}',
    dag=dag,
    **{{ task.params }}
)
{% endfor %}
{% endfor %}

# Set task and job dependencies
{% for job in jobs %}
{% for task in job.tasks %}
{% for dependency in task.dependencies %}
{{ job.job_id }}_{{ dependency }} >> {{ job.job_id }}_{{ task.task_id }}
{% endfor %}
{% endfor %}
{% endfor %}

{% for job in jobs %}
{% for dependency in job.dependencies %}
{{ dependency }}_{{ jobs[dependency|int].tasks[-1].task_id }} >> {{ job.job_id }}_{{ job.tasks[0].task_id }}
{% endfor %}
{% endfor %}

                        """)

    dag_content = template.render(
        dag_id=config['dag_id'],
        default_args=config['default_args'],
        jobs=config['jobs']
    )

    with open(f"dags/{config['dag_id']}.py", 'w') as f:
        f.write(dag_content)


# Path to your JSON configuration file
    
# Directory of the current script directory
script_directory = os.path.dirname(os.path.abspath(__file__)) # for relative path use os.path.relpath 

# Path to the file
json_input_data = os.path.join(script_directory, 'config/new_input_data.json') # This will change to pick up json_input during runtime
output_dir = os.path.join(script_directory, 'dags/')

# Generate the DAG file dynamically
# generate_dag_file(json_input_data, f"{output_dir}new_dag_file.py")

if __name__ == "__main__":
    config = load_config(os.path.join(script_directory, 'config/new_input_data.json'))
    generate_dag_file(config)