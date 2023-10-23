import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import requests

from api.logic.db_interactions.node_db import nodes_select


def server_choice(file_size):
    nodes = nodes_select()
    available_right_now = []

    for node in nodes:
        if node['available']:
            check_space = requests.get(f'http://{node["ip"]:8000/info/space}')
            if check_space.status_code == 200:
                available_right_now.append((node['ip'], check_space.text))

    available_right_now = sorted(available_right_now, key=lambda memory: memory[1])
    return available_right_now[0]


def upload_to_server(server_ip, user_id, file):
    server_url = f'http://{server_ip}:10000/files/files'
    data = {'user': user_id, 'file': file}
    response = requests.post(server_url, json=data)
    if response.status_code != 200:
        return False
    return True


def executor(user_id, file):
    file_size = os.stat(file)
    server = server_choice(file_size)
    upload_to_server(server, user_id, file)

