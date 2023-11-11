import base64
import io
import os
import shutil
from pathlib import Path

import httpx

from api.logic.db_interactions.node_db import nodes_select


def server_choice(file_size) -> []:
    nodes = nodes_select()
    available_right_now = []

    for node in nodes:
        print(node)
        check_space = httpx.get(f'http://{node["ip"]}:10000/info/space')
        if check_space.status_code == 200:
            available_right_now.append((node['ip'], check_space.text))

    if len(available_right_now) != 0:
        available_right_now = sorted(available_right_now, key=lambda memory: memory[1])
        return available_right_now[0]
    return []


def upload_to_server(server_ip, user_id, file) -> bool:
    server_url = f'http://{server_ip}:10000/files/files'
    print('SERVERURL', server_url)
    with open(file, 'rb') as target_file:
        file_data = target_file.read()
    files = {'file': ('example.txt', file_data)}
    response = httpx.post(f'{server_url}?user={user_id}', files=files)
    print(response.text)
    if response.status_code != 200:
        return False
    return True


def temp_save(file):
    pwd = "D:/diploma/diplom-client/huh/"
    content = file.file.read()
    pat = f'{pwd}{file.filename}'
    with open(pat, 'wb') as temp_file:
        temp_file.write(content)
    file_size = os.stat(f'{pwd}{file.filename}')
    return file_size, pat


def executor(user_id, file) -> bool:
    size, path = temp_save(file)
    server, space = server_choice(size)
    if server is []:
        return False
    final = upload_to_server(server, user_id, path)
    if final:
        return True
    return False

