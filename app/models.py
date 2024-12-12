from .database import Base;
from sqlalchemy import Column, Integer, String, Boolean
class Post(Base):
    __table__name = "posts"

    id =  Column(Integer, primary_key = True, nullable=False)
    name = Column(String, nullable=False)
    content =  Column(String, nullable= False)
    published = Column(Boolean, default=True)

 