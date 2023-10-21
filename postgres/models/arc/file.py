import uuid

from sqlalchemy import Column, String, INT, BOOLEAN, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class File(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    nodes = Column(JSONB)
