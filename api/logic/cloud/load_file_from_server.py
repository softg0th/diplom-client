import base64

import requests


def check_file_nodes(user_id, file_name, nodes):
    file_parts = {}
    for node in nodes:
        file = requests.get(f'http://{node}/files/files/load/?user={user_id}&file_name={file_name}').json()
        file_parts[str(file['file_part'])] = base64.b64decode(file['file_binary_data'])
    file_parts = dict(sorted(file_parts.items()))
    return file_parts
