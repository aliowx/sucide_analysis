import logging

import secrets
from typing import Union, AsyncGenerator
from fastapi.security import HTTPBasicCredentials
from redis.asyncio import redis, client
from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud 
from app import exceptions as exc 
from app import models, schemas, utils
from app.utils import redis_client
from app.core.config import (
    settings,
    ACCESS_TOKEN_BLOCKLIST_KEY,
    REFRESH_TOKEN_BLOCKLIST_KEY
)
from app.core.security import JWTHandler, basic_security
from app.db.session import async_session



logger = logging.getLogger(__name__)



async def get_db_async() -> AsyncGenerator:
    """
    Dependency function for get database
    """
    async with async_session() as session:
        yield session
        
        
async def get_redis()-> client.Redis:
    """
    Dependency function that get redis client
    """
    try:
        if await redis_client.ping():
            return redis_client
        raise redis.RedisError('ping error')
    except Exception as e:
        logger.error(f'Redis connection failed\n{e}')
        raise e
    
async def get_user_id_from_cookie(
    request: Request,
    response: Response,
    cache: client.Redis = Depends(get_redis)
):
    try:
        access_token = request.cookies.get("Access-Token")
        if not access_token:
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.access_token_not_found
            )
            
        token = JWTHandler.decode(access_token)
        if await cache.get(ACCESS_TOKEN_BLOCKLIST_KEY.format(token=access_token)):
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.expired_token
            )
        user_id = token.get('id')
        
        if token.get('sub')  != 'access' or not user_id:
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.inactive_user
            )
            
    except:
        refresh_token = request.cookies.get("Refresh-Token")
        if not refresh_token:
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.refresh_token_not_found
            )
            
        refresh_token_data = JWTHandler.decode(refresh_token)
        if (
            await cache.get(REFRESH_TOKEN_BLOCKLIST_KEY.format(token=refresh_token))
            or refresh_token_data.get('sub') != 'refresh'
        ):
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.inactive_user
            )
            
        user_id = refresh_token_data.get('id')
        
        token = JWTHandler.encode(payload={"sub": "access", "id": user_id})
        
        
        response.set_cookie(
            key="Access-Token",
            value=token,
            secure=True,
            httponly=True,
            samesite="strict" if not settings.DEBUG else "none",
            expires=JWTHandler.token_expiration(token),
            
        ) 
    
    request.state.user_id = user_id
    
    return int(user_id)



async def get_current_user_from_cookie(
    db: AsyncSession = Depends(get_db_async),
    current_user_id: int = Depends(get_user_id_from_cookie)
)-> schemas.User:
    current_user = await crud.user.get(db=db, id_=current_user_id)
    
    if not current_user:
        raise exc.ForbiddenException(msg_code=utils.MessageCodes.invalid_token)
    
    
    if not crud.user.is_active(current_user):
        raise exc.ForbiddenException(
            msg_code=utils.MessageCodes.inactive_user
        )
        
        
    return current_user