from sqlalchemy import VARCHAR, Column, LargeBinary, Text
from models.base import Base 

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Text,primary_key=True)
    name =Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)
 