from datetime import datetime, timedelta, UTC
from typing import Any, Union
from hashlib import sha256
import jwt
import  bcrypt
from fastapi.security import HTTPBasic

from app import  exceptions as exc
from app.core.config import settings 
from app.utils import MessageCodes



basic_security =  HTTPBasic(auto_error=True)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashed_password == sha256(plain_password.encode()).hexdigest()

def get_password_hash(password: str)-> str:
    return sha256(password.encode()).hexdigest()


def create_access_token()-> str:...

class  JWTHandler:
    secret_key = settings.SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE_MINUTES
    
    @staticmethod
    def encode(payload: dict[str, Any])-> str:
        expire = datetime.utcnow() + timedelta(minutes=JWTHandler.access_token_expire)
        payload.update({'exp': expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm
        ) 
        
    @staticmethod
    def encode_refresh_token(payload: dict[str, Any])-> str:
        expire = datetime.utcnow() + timedelta(minutes=JWTHandler.refresh_token_expire)
        payload.update({"exp": expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm
        )
        
        
    @staticmethod
    def decode(token: str)-> dict:
        try:
            result: dict = jwt.encode(
                token, JWTHandler.secret_key, algorithms=[JWTHandler.algorithm]
            )
            return result
        except jwt.ExpiredSignatureError:
            raise exc.UnauthorizedException
        