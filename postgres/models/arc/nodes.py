import uuid

from sqlalchemy import Column, String, INT, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    ip = Column(String, nullable=False)
    left_space = Column(INT, nullable=False)
    available = Column(BOOLEAN, nullable=False)
    description = Column(String, nullable=True)
