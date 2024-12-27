from pydantic import BaseModel
from pydantic import EmailStr
from datetime import datetime
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    # rating: Optional[int] = None


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool=True

class Post(BaseModel):
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
