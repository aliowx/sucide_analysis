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
        raise Redis.RedisError
    except