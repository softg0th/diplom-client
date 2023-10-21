from abc import abstractmethod, ABC
from typing import List

import pydantic
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.testing.schema import Table
from sqlalchemy import Column, String, BOOLEAN, INT
from sqlalchemy.dialects.postgresql import UUID

engine = create_engine("postgresql://postgres:12345@127.0.0.1:5432/system_main")
conn = engine.connect()
metadata = MetaData()

NodeTab = Table('nodes', metadata,
                Column('id', UUID, primary_key=True),
                Column('ip', String),
                Column('left_space', INT),
                Column('available', BOOLEAN),
                Column('description', String)
                )


def nodes_select():
    findNode = sqlalchemy.select(NodeTab)
    got_nodes = conn.execute(findNode).fetchall()
    nodes = []

    for row in got_nodes:
        row_dct = {'id': str(row[0]), 'ip': row[1], 'left_space': row[2], 'available': row[3],
                   'description': row[4]}
        nodes.append(row_dct)
    return nodes


class NodeInteractionsPattern(ABC):
    @abstractmethod
    def getNodes(self) -> List:
        pass

    @abstractmethod
    def createNode(self, node_data) -> bool:
        pass

    @abstractmethod
    def deleteNode(self, node_id) -> bool:
        pass


class NodeInteractions(NodeInteractionsPattern):

    def getNodes(self) -> List:
        nodes = nodes_select()
        return nodes

    def createNode(self, node_data) -> bool:
        try:
            data = node_data['node']
            create = sqlalchemy.insert(NodeTab).values(id=str(data.id), ip=data.ip, left_space=data.left_space,
                                                       available=data.available, description=data.description)
        except pydantic.error_wrappers.ValidationError:
            return False

        with engine.connect() as conn:
            conn.execute(create)
            conn.commit()

        return True

    def deleteNode(self, node_id):
        try:
            delete = sqlalchemy.delete(NodeTab).where(NodeTab.c.id == str(node_id))

            with engine.connect() as conn:
                conn.execute(delete)
                conn.commit()

        except Exception:
            return False
        return True
