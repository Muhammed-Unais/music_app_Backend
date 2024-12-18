import uuid
import bcrypt
from fastapi import Depends, HTTPException
from database import get_db
from models.user import User
from pydactic_schemas.user_create import UserCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session


router = APIRouter()

@router.post('/signup') 
def signup_user(user:UserCreate,db: Session = Depends(get_db)):    
    user_db = db.query(User).filter(User.email == user.email).first()
    
    if user_db:
        raise HTTPException(400,'User with same email address already exist')
    
    hash_pw = bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    
    user_db = User(id =str(uuid.uuid4()),name= user.name,email = user.email,password= hash_pw)    
    
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    
    return user_db
    