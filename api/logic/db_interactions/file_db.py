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
from api.logic.db_interactions.node_db import NodeTab
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
            return bytes(primer)
        return decoded_bytes[0]
    except reedsolo.ReedSolomonError:
        return None


class FileInteractions(FileInteractionsPattern):
    def get_all_files(self, user_id) -> List:
        if uf.isUserExist(user_id):
            findFile = sqlalchemy.select(FileTab).where(FileTab.c.user == str(user_id))
            foundFiles = conn.execute(findFile).fetchall()
            files = []

            for row in foundFiles:
                row_dct = {'verbose_name': row[3]}
                files.append(row_dct)
            return files
        return []

    def create_file(self, user_id, file_id, verbose_name) -> List:
        if uf.isUserExist(user_id):
            create = sqlalchemy.insert(FileTab).values(id=str(file_id), user=str(user_id), nodes=[],
                                                       verbose_name=str(verbose_name))
            with engine.connect() as conn:
                conn.execute(create)
                conn.commit()
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
            found_file_nodes = conn.execute(file_nodes).fetchone()
            return found_file_nodes[2]

    def append_nodes(self, user_id, file_id, node):
        if uf.isUserExist(user_id):
            file_nodes = sqlalchemy.select(FileTab).where(FileTab.c.id == str(file_id))
            found_file_nodes = conn.execute(file_nodes).fetchone()
            if found_file_nodes:
                current_nodes = found_file_nodes.nodes
                current_nodes.append(node)
                update_node = FileTab.update().where(FileTab.c.id == str(file_id)).values(nodes=current_nodes)
                conn.execute(update_node)
                conn.commit()

    def load_file(self, user_id, file_id, file_name):
        fi = FileInteractions()
        nodes = fi.get_file_nodes(user_id, file_id)
        file_parts = check_file_nodes(user_id, file_name, nodes)
        all_len = 0
        pwd = "D:/diploma/diplom-client/temp/"
        final_file = bytes()
        datas = []
        for dt in file_parts:
            datas.append(file_parts[dt])

        for part in datas:
            print(part)
            part_bytes = decode(part, all_len, len(part) + 2)
            print(part_bytes)
            all_len += len(part)
            final_file += part_bytes

        print(final_file)
        with open(f"{pwd}/{file_name}", 'wb') as f:
            f.write(final_file)

        file_pwd = f"{pwd}{file_name}"
        return file_pwd, file_name
