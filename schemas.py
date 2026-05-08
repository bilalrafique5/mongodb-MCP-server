from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    name: str
    age: int
    reg_no: int
    phone: Optional[str] = None
    email: Optional[str] = None


class Filter(BaseModel):
    name_starts_with: Optional[str] = None
    name_contains: Optional[str] = None
    age_gt: Optional[int] = None
    age_lt: Optional[int] = None
    reg_no: Optional[int] = None


class InsertUsers(BaseModel):
    users: List[User]