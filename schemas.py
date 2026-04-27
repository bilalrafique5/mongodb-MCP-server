from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    name: str
    age: int


class InsertUsers(BaseModel):
    users: List[User]


class Filter(BaseModel):
    name_starts_with: Optional[str] = None


class GetUsers(BaseModel):
    filter: Optional[Filter] = None


class DeleteUsers(BaseModel):
    names: List[str]