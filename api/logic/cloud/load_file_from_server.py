import reedsolo
import httpx
import hashlib

import requests

from api.logic.db_interactions.file_db import FileInteractions


def decode(encoded_text, n, original_length=None):
    rsc = reedsolo.RSCodec(n)
    try:
        decoded_bytes = rsc.decode(encoded_text)
        if original_length:
            primer = decoded_bytes[0][-original_length:]
            print(primer.decode('utf-8'))
            return bytes(primer)
        return decoded_bytes[0]
    except reedsolo.ReedSolomonError:
        return None


def check_file_nodes(user_id, file_id, file_name):
    fi = FileInteractions()
    nodes = fi.get_file_nodes(user_id, file_id)
    file_parts = {}

    for node in nodes:
        file = requests.get(f'{node}/files/load/{user_id},{file_id}').json()
        output = file.loads(file)
        file_parts[output['file_part']] = output['file_binary_data']

    pwd = "D:/diploma/diplom-client/temp/"
    file_parts = dict(sorted(file_parts.items()))
    all_len = 0

    with open(f"{pwd}/filename", 'w') as f:
        for part in file_parts:
            all_len += len(part)
            f.write(part)

    with open(f"{pwd}/{file_name}", 'r') as f:
        file_data = f.read()

    with open("D:\diploma\diplom-client\hash.txt") as f:
        file_hash = f.read()

    if hashlib.md5(file_data).hexdigest() != file_hash:
        for part in file_parts:
            file_parts[part] = decode(part, all_len, len(part) + 2)

        with open(f"{pwd}/{file_name}", 'w') as f:
            for part in file_parts:
                f.write(part)

        new_file = f"{pwd}/{file_name}"
        return new_file

    return f"{pwd}/{file_name}"
