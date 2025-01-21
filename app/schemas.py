
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
# pydantic : a library fot Type of the model

############################################################# ..... User Schemas.... #############################################################

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str 

class UserOut(BaseModel):
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class User(UserOut): # UserOut is the parent class of User class 
    id: int
    created_at: datetime
        
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

############################################################# ..... Post Schemas.... #############################################################

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase): # PostBase is the parent class of Post class 
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
        
    model_config = ConfigDict(from_attributes=True)


############################################################# ..... Token Schemas.... #############################################################

class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)