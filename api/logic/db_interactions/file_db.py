import hashlib
from abc import abstractmethod, ABC
from typing import List
from uuid import UUID

import reedsolo
import sqlalchemy
from sqlalchemy import create_engine, MetaData, String, ForeignKey
from sqlalchemy.testing.schema import Table, Column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from api.logic.cloud.load_file_from_server import check_file_nodes
from api.logic.db_interactions.user_db import UsersFinder

engine = create_engine("postgresql://postgres:12345@127.0.0.1:5432/system_main")
conn = engine.connect()
metadata = MetaData()
uf = UsersFinder()

FileTab = Table('files', metadata,
                Column('id', UUID, primary_key=True),
                Column('user', UUID, ForeignKey('user.id')),
                Column('nodes', JSONB),
                Column('verbose_name', String)
                )


class FileInteractionsPattern(ABC):
    @abstractmethod
    def get_all_files(self, user_id) -> List:
        pass

    @abstractmethod
    def create_file(self, user_id, file_id, verbose_name) -> List:
        pass

    @abstractmethod
    def update_file(self, user_id, file_id, verbose_name) -> bool:
        pass

    @abstractmethod
    def delete_file(self, user_id, file_id) -> List:
        pass

    @abstractmethod
    def get_file_nodes(self, user_id, file_id) -> List:
        pass

    @abstractmethod
    def load_file(self, user_id, file_id, file_name):
        pass


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


class FileInteractions(FileInteractionsPattern):
    def get_all_files(self, user_id) -> List:
        if uf.isUserExist(user_id):
            findFile = sqlalchemy.select(FileTab).where(FileTab.c.user == str(user_id))
            foundFiles = conn.execute(findFile).fetchall()
            print('query')
            files = []

            for row in foundFiles:
                row_dct = {'verbose_name': row[3]}
                files.append(row_dct)
            return files
        return []

    def create_file(self, user_id, file_id, verbose_name) -> List:
        if uf.isUserExist(user_id):
            print('exist')
            create = sqlalchemy.insert(FileTab).values(id=str(file_id), user=str(user_id), nodes=[],
                                                       verbose_name=str(verbose_name))
            with engine.connect() as conn:
                conn.execute(create)
                conn.commit()
            print('query')
            return [user_id, file_id]
        return []

    def update_file(self, user_id, file_id, verbose_name) -> bool:
        if uf.isUserExist(user_id):
            update = (sqlalchemy.update(FileTab).where(FileTab.c.id == str(file_id)).values
                      (verbose_name=str(verbose_name)))

            with engine.connect() as conn:
                conn.execute(update)
                conn.commit()

            return True
        return False

    def delete_file(self, user_id, file_id) -> List:
        if uf.isUserExist(user_id):
            delete = sqlalchemy.delete(FileTab).where(FileTab.c.id == str(file_id))
            with engine.connect() as conn:
                conn.execute(delete)
                conn.commit()
            return [user_id, file_id]
        return []

    def get_file_nodes(self, user_id, file_id) -> List:
        if uf.isUserExist(user_id):
            file_nodes = sqlalchemy.select(FileTab).where(FileTab.c.id == str(file_id))
            found_file_nodes = conn.execute(file_nodes).fetchall()
            return [found_file_nodes[2]]

    def load_file(self, user_id, file_id, file_name):
        fi = FileInteractions()
        nodes = fi.get_file_nodes(user_id, file_id)
        file_parts = check_file_nodes(user_id, file_id, nodes)
        all_len = 0
        pwd = "D:/diploma/diplom-client/temp/"
        with open(f"{pwd}/filename", 'w') as f:
            for part in file_parts:
                if all_len < 1000:
                    part = decode(part, all_len, len(part) + 2)
                all_len += len(part)
                f.write(part)

        file_pwd = f"{pwd}/{file_name}"
        return file_pwd
