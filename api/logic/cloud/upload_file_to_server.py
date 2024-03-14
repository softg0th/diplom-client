import hashlib
import os
from pathlib import Path

import httpx
import reedsolo
import requests

from api.logic.db_interactions.file_db import FileInteractions
from api.logic.db_interactions.node_db import nodes_select


def encode(text, n):
    rsc = reedsolo.RSCodec(n)
    encoded_bytes = rsc.encode(text)
    return encoded_bytes


def server_choice() -> []:
    nodes = nodes_select()
    available_right_now = []

    for node in nodes:
        check_space = requests.get(f'http://{node["ip"]}/info/space')
        if check_space.status_code == 200:
            available_right_now.append(node['ip'])

    if len(available_right_now) != 0:
        available_right_now = sorted(available_right_now, key=lambda memory: memory[1])
        return available_right_now
    return []


def upload_to_server(server_ip, user_id, file, file_id) -> bool:
    server_url = f'http://{server_ip}/files/files'
    fi = FileInteractions()
    fi.append_nodes(user_id, file_id, server_ip)
    with open(file, 'rb') as target_file:
        file_data = target_file.read()
    files = {'file': (f'{file}', file_data)}
    response = requests.post(f'{server_url}?user={user_id}', files=files)
    if response.status_code != 200:
        return False
    return True


def temp_save(file):
    pwd = "D:/diploma/diplom-client/temp/"
    content = file.file.read()
    file_length = len(content) // 3

    if len(content) < 1000:
        file_split_datas = [encode(content[:file_length], file_length),
                            encode(content[file_length:2 * file_length], file_length),
                            encode(content[2 * file_length:], file_length)]
    else:
        file_split_datas = [content[:file_length],
                            content[file_length:2 * file_length],
                            content[2 * file_length:]]
    paths_files = []
    for it in range(3):
        pat = f'{pwd}{file.filename}.{it}'
        with open(pat, 'wb') as temp_file:
            temp_file.write(file_split_datas[it])
        paths_files.append(pat)
    file_size = os.stat(f'{pwd}{file.filename}.1')
    return file_size, paths_files


def executor(user_id, file, file_id):
    size, path_files = temp_save(file)
    filename = Path(file.filename)
    fi = FileInteractions()
    fi.create_file(user_id, file_id, filename)
    server = server_choice()

    if server is []:
        return False

    for three in range(3):
        upload_to_server(server[three], user_id, path_files[three], file_id)

    return True
