import uuid
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session, joinedload
from middleware.auth_middleware import auth_middleware
from database import get_db
from models.favorite import Favorite
from models.song import Song
from pydactic_schemas.favorite_song import FavoriteSong


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

        db.add(new_song)    
        db.commit()
        db.refresh(new_song)

        return new_song
    except:
        print("exception") 
        
@router.get('/list',status_code=200)
def list_songs(db : Session = Depends(get_db),
               auth_dict = Depends(auth_middleware)
               ):
    songs = db.query(Song).all()
    return songs


@router.post('/favorite')
def favorite_song(fav_song : FavoriteSong,
                  db:Session =Depends(get_db),
                  auth_dict= Depends(auth_middleware),
                  ):
    
    user_id = auth_dict['uid']
    favo_song = db.query(Favorite).filter(Favorite.song_id == fav_song.song_id
                                         ,Favorite.user_id == user_id).first()
    if favo_song:
        db.delete(favo_song)
        db.commit()
        return {"message": False}
    else:
        new_fav = Favorite(id= str(uuid.uuid4()),
                           song_id = fav_song.song_id,
                           user_id = user_id,
                           )
        
        db.add(new_fav)
        db.commit()
        return {'message':True}
        
@router.get('/list/favorites',status_code=200)
def list_songs(db : Session = Depends(get_db),
               auth_dict = Depends(auth_middleware)
               ):
    user_id = auth_dict['uid']
    fav_songs = db.query(Favorite).filter(Favorite.user_id == user_id).options(
        joinedload(Favorite.song)
        ).all()
    return fav_songs        