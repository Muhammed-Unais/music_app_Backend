from sqlalchemy import VARCHAR, Column, Text
from models.base import Base

class Song(Base):
    __tablename__ = 'songs'
    
    id = Column(Text,primary_key=True)
    song_url = Column(Text)
    thumbnail_url = Column(Text)
    artist = Column(Text)
    song_name = Column(VARCHAR(100))
    hex_code = Column(VARCHAR(6))