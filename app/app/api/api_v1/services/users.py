from sqlalchemy.ext.asyncio import AsyncSession

from app import (
    crud,
    core,
    schemas,
    models,
    exceptions as exc,
    utils
)

async def read_user_by_id(
    user_id: int,
    current_user: models.User,
    db:AsyncSession
)->schemas.User:
    user = await crud.user.get(db, id = user_id)
    if not user:
        raise exc.NotFoundException(
            detail='User not found',
            msg_code=utils.MessageCodes.not_found
        )
        
    if user == current_user:
        return user
    
    if not crud.user.is_superuser(
        current_user
    ):
        raise exc.ForbiddenException(
            detail="The user doesn't have enough privileges",
            msg_code=utils.MessageCodes.bad_request
        )
        
        
    return user