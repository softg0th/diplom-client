import uuid

from pydantic import BaseModel, Field
from uuid import UUID


class ValidUser(BaseModel):
    id = uuid.uuid4()
    username: str = Field(description='user name')
    password: str = Field(description='user password')
    files: list

class UserAuth(BaseModel):
    username: str = Field(description='user name')
    password: str = Field(description='user password')

class UpdatedUser(BaseModel):
    field: str = Field(description='user password')


class ValidNode(BaseModel):
    id = uuid.uuid4()
    ip: str = Field(description='node ip')
    left_space: int = Field(description='node left space')
    available: bool = Field(description='node avalability')
    description: str

