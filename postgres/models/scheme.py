import uuid

from sqlalchemy import Column, String, BOOLEAN, INT, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    files = Column(JSONB)


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    ip = Column(String, nullable=False)
    left_space = Column(INT, nullable=False)
    available = Column(BOOLEAN, nullable=False)
    description = Column(String, nullable=True)


class File(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    nodes = Column(JSONB, nullable=False)
    verbose_name = Column(String, nullable=False)
