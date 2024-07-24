import json
from airflow.settings import Session
from airflow.models import Connection
import os

connection = json.loads("""{
    "conn_id": "my_database_conn_5", 
    "conn_type": "mysql",
    "host": "mysql",
    "port": "3306",
    "login": "root",
    "password": "password",
    "schema": "file_transfer"
}""")
session = Session()

# Create new Airflow connection
conn_exists = session.query(Connection).filter(Connection.conn_id == connection['conn_id']).first()
print(conn_exists)
