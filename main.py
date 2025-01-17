from fastapi import FastAPI, HTTPException
from routes import auth, song
from models.base import Base
from database import engine

app = FastAPI()

app.include_router(auth.router,prefix='/auth')
app.include_router(song.router,prefix="/song")
    
    
Base.metadata.create_all(engine)
print('called')