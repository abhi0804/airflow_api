def add_conn(data , container):
    path_script = 'create_connection.py'
    exec_command = f"python {path_script}"
    exec_result = container.exec_run(exec_command, environment={"JSON_DATA": data})

    # Acknowledge
    if exec_result:
        return exec_result.output.decode('utf-8')
    else:
        return 'failed'

    
def update_conn():
    pass

def delete_conn():
    pass