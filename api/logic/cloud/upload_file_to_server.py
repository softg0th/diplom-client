import hashlib
import os

import httpx
import reedsolo

from api.logic.db_interactions.node_db import nodes_select


def encode(text, n):
    rsc = reedsolo.RSCodec(n)
    encoded_bytes = rsc.encode(text)
    return encoded_bytes


def server_choice(file_size) -> []:
    nodes = nodes_select()
    available_right_now = []

    for node in nodes:
        check_space = httpx.get(f'http://{node["ip"]}:10000/info/space')
        if check_space.status_code == 200:
            available_right_now.append((node['ip'], check_space.text))

    if len(available_right_now) != 0:
        available_right_now = sorted(available_right_now, key=lambda memory: memory[1])
        return available_right_now[0]
    return []


def upload_to_server(server_ip, user_id, file) -> bool:
    server_url = f'http://{server_ip}:10000/files/files'
    with open(file, 'rb') as target_file:
        file_data = target_file.read()
    files = {'file': ('example.txt', file_data)}
    response = httpx.post(f'{server_url}?user={user_id}', files=files)
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
                            encode(file_length[2 * file_length:], file_length)]
    else:
        file_split_datas = [content[:file_length],
                            content[file_length:2 * file_length],
                            file_length[2 * file_length:]]
    paths_files = []
    for it in range(3):
        pat = f'{pwd}{file.filename}.{it}'
        with open(pat, 'wb') as temp_file:
            temp_file.write(file_split_datas[it])
        paths_files.append(pat)
    file_size = os.stat(f'{pwd}{file.filename}.1')
    return file_size, paths_files


def executor(user_id, file):
    size, path_files = temp_save(file)
    server, space = server_choice(size)

    if server is []:
        return False

    for pat in path_files:
        upload_to_server(server, user_id, pat)

    return True
