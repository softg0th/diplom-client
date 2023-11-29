from abc import abstractmethod, ABC
from typing import List
from uuid import UUID

import sqlalchemy
from sqlalchemy import create_engine, MetaData, String, ForeignKey
from sqlalchemy.testing.schema import Table, Column
from sqlalchemy.dialects.postgresql import UUID, JSONB

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
