from pydantic import BaseModel, Field
from uuid import UUID


class ValidUser(BaseModel):
    id: UUID
    username: str = Field(description='user name')
    password: str = Field(description='user password')
    files: list


class UpdatedUser(BaseModel):
    field: str = Field(description='user password')
