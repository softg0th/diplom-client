import requests


def check_file_nodes(user_id, file_id, nodes):
    file_parts = {}
    for node in nodes:
        file = requests.get(f'http://{node}/files/load/{user_id},{file_id}').json()
        output = file.loads(file)
        file_parts[output['file_part']] = output['file_binary_data']

    file_parts = dict(sorted(file_parts.items()))
    return file_parts
