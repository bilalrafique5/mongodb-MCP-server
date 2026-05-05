from pydantic import BaseModel
from typing import Optional, List


class Filter(BaseModel):
    name_starts_with: Optional[str] = None
    age_gt: Optional[int] = None
    age_lt: Optional[int] = None


class GetUsers(BaseModel):
    filter: Optional[Filter] = None


class User(BaseModel):
    name: str
    age: int
    reg_no: int


class InsertUsers(BaseModel):
    users: List[User]