import time 

from redis.asyncio import  client
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app import exceptions as exc
from app import schemas, models ,utils

from app.core.config import REFRESH_TOKEN_BLOCKLIST_KEY, ACCESS_TOKEN_BLOCKLIST_KEY
from app.core.security import JWTHandler


async def register(
    db: AsyncSession,
    user_in: schemas.UserCreate
)-> schemas.User:
    user = await crud.user.get_by_username(db=db, username=user_in.Username)
    if user:
        raise exc.AlreadyExistException(
            detail="The user with this username already exists",
            msg_code=utils.MessageCodes.bad_request
        )
    user = await crud.user.create(db=db, obj_in=user_in)
    return user



