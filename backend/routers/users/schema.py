from enum import Enum
import pydantic
from pydantic import Field
from typing import Optional


class UserBaseInfo(pydantic.BaseModel):
    id: int
    username: str
    requiredCalories: float

class UserInfo(UserBaseInfo):
    role: str
    requierdCalories: Optional[float]=None
    class Config():
        from_attributes = True

class ListUsers(pydantic.BaseModel):
    count: int
    users: list[UserInfo]

class Cache_Media(str, Enum):
    super_admin = 'super_admin'
    admin = 'admin'
    user = 'user'

class CreateUser(pydantic.BaseModel):
    username: str
    email: str
    age: int
    weight: float
    height: float
    gender: str
    activity: str
    goal: str
    password: str
    class Config():
        from_attributes = True

class CreateUserRes(pydantic.BaseModel):
    id: int
    username: str
    role: Cache_Media
    
    class Config():
        from_attributes = True

class Login(pydantic.BaseModel):
    email: str
    password: str
    class Config():
        from_attributes = True

class AuthRespose(pydantic.BaseModel):
    id: int
    token:str
    role:str
    username:str
    class Config():
        from_attributes = True