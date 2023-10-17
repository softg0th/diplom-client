from pydantic import BaseModel, Field
from uuid import UUID


class ValidUser(BaseModel):
    id: UUID
    username: str = Field(description='user name')
    password: str = Field(description='user password')
    files: list


class UpdatedUser(BaseModel):
    field: str = Field(description='user password')


class ValidNode(BaseModel):
    id: UUID
    ip: str = Field(description='node ip')
    left_space: int = Field(description='node left space')
    available: bool = Field(description='node avalability')
    description: str

