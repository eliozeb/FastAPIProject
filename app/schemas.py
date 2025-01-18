
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
# pydantic : a library fot Type of the model


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase): # PostBase is the parent class of Post class 
    id: int
    created_at: datetime
        
    model_config = ConfigDict(from_attributes=True)



############################################################# ..... User .... #############################################################

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str 