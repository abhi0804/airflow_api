from flask import Flask, request, jsonify
import subprocess
import json
import docker
import logging
from call_functions import add_conn, update_conn, delete_conn

logger = logging.getLogger(__name__)

app = Flask(__name__)
name_container = 'airflow-webserver'

conn_mapping = {
    'POST': add_conn,
    'PUT': update_conn,
    'DELETE': delete_conn
}


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/connection", methods=['POST', 'PUT', 'DELETE'])
def connection():
    my_dict = request.get_json()
    request_type = request.method
    logger.info(f"Request type is :{request_type}")
    data = json.dumps(my_dict)
    client = docker.from_env()

    # Container where script will be triggered
    container = client.containers.get(name_container)

    # Function will be picked based on http_request type
    call_func = conn_mapping.get(request_type)

    # Call the function
    func_response = call_func(data, container)

    return func_response, 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
