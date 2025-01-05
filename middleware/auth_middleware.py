from fastapi import HTTPException
from fastapi.params import Header
import jwt


def auth_middleware(x_auth_token = Header()):
    
    print(x_auth_token)
    try:
        if not x_auth_token:
            raise HTTPException(401,"No auth token , verification failed")
        
        verfied_token = jwt.decode(x_auth_token,'password_key',['HS256'])
        if not verfied_token:
            raise HTTPException(401,'Token verification failed, autherization failed')
    
        uid = verfied_token.get('id')
        return {"uid":uid,"token":x_auth_token}
    
    except jwt.PyJWTError:
        raise HTTPException(401,"Token is not valid, authorization failed")