import json
from airflow.settings import Session
from airflow.models import Connection
import os
from check_connection_exists import connection_exists


def create_airflow_connection():
    # Read JSON data from environment variable
    json_data = os.environ.get('JSON_DATA')

    # Read connection details from JSON file
    connection = json.loads(json_data)

    # Check if Airflow Connection Exists
    conn_exists = connection_exists(connection['conn_id'])
    if conn_exists:
        print(f"Connection with ID '{connection['conn_id']}' exists.")
    else:

        # If False, create a new connection
        new_conn = Connection(**connection)
        session = Session()
        session.add(new_conn)
        session.commit()
        session.close()

        print('connection_created_successfully')


if __name__ == "__main__":
    create_airflow_connection()
