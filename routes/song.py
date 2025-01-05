import uuid
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from middleware.auth_middleware import auth_middleware
from database import get_db
from models.song import Song


router = APIRouter()

cloudinary.config( 
    cloud_name = "dvihywo6p", 
    api_key = "946723352357176", 
    api_secret = "HUEBHwIULpeCa-5MsrZ0z7xrCsU",
    secure = True
)

@router.post('/upload',status_code=201)
def upload_song(song:UploadFile =File(...),
                thumbnail:UploadFile =File(...),
                artist:str = Form(...),
                song_name: str =Form(...),
                hex_code:str =Form(...),
                db: Session = Depends(get_db),
                auth_dict = Depends(auth_middleware)
                ):
    try: 
        song_id = str(uuid.uuid4())
        song_res = cloudinary.uploader.upload(song.file,resource_type ='auto',folder =f'songs/{song_id}')
        thumbnail_res = cloudinary.uploader.upload(thumbnail.file,resource_type ='image',folder =f'songs/{song_id}')
    
        new_song = Song(
            id = song_id,
            song_url =song_res['url'],
            thumbnail_url = thumbnail_res['url'],
            artist = artist,
            song_name = song_name,
            hex_code = hex_code,
        )
    
        print(new_song.song_name)
        print(new_song.artist)

        db.add(new_song)
        db.commit()
        db.refresh(new_song)

        return new_song
    except:
        print("exception") 