from airflow.settings import Session
from airflow.models import Connection

def connection_exists(conn_id):
    # Create a session
    session = Session()

    # Query the Connection table
    connection = session.query(Connection).filter(Connection.conn_id == conn_id).first()

    # Close the session
    session.close()

    # Return True if the connection exists, otherwise False
    return connection is not None