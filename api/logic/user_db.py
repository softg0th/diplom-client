from abc import abstractmethod, ABC

import pydantic
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Column, String
from sqlalchemy.testing.schema import Table
from sqlalchemy.dialects.postgresql import UUID, JSONB


engine = create_engine("postgresql://postgres:12345@127.0.0.1:5432/system_main")
conn = engine.connect()
metadata = MetaData()

UserTab = Table('users', metadata,
                Column('id', UUID, primary_key=True),
                Column('username', String),
                Column('password', String),
                Column('files', JSONB)
                )


class UserInteractionsPattern(ABC):
    @abstractmethod
    def createUser(self, user_data) -> bool:
        pass

    @abstractmethod
    def updateUser(self, user_id, new_fields, field_name) -> bool:
        pass


class UserInteractions(UserInteractionsPattern):
    def createUser(self, data) -> bool:
        try:
            data = data['user']
            create = sqlalchemy.insert(UserTab).values(id=str(data.id), username=data.username, password=data.password,
                                                       files=[])
        except pydantic.error_wrappers.ValidationError:
            return False

        conn.execute(create)
        conn.commit()
        return True

    def updateUser(self, user_id, new_fields, field_name) -> bool:
        if field_name not in ('username', 'password'):
            return False
        findUser = sqlalchemy.select(UserTab).where(UserTab.c.id == str(user_id))
        userExists = conn.execute(findUser)
        if userExists:
            try:
                if field_name == 'username':
                    update = sqlalchemy.update(UserTab).where(UserTab.c.id == str(user_id)).values(
                        username=new_fields.field)
                elif field_name == 'password':
                    print('password')
                    update = sqlalchemy.update(UserTab).where(UserTab.c.id == str(user_id)).values(
                        password=new_fields.field)
                conn.execute(update)
                conn.commit()
            except Exception:
                    return False
        return True
