from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, select
from app.crud.base import CRUDBase
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserCreate, UserUpdate
from app.db.base_class import Base


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_username(self, db:AsyncSession, username: str)-> User | None:
        query = select(self.model).where(
            and_(
                self.model.Username == username,
                self.model.is_deleted.is_(None)
            )
        )
        response = await db.execute(query) 
        return response.scalar_one_or_none()
    
    
    # async def create(self, db: AsyncSession, obj_in: UserCreate | dict) -> Base | Any:
    #     if isinstance(obj_in, dict):
    #         password = obj_in['password']
            
    #     else:
    #         password = obj_in.password
            
    #     obj_in_data = jsonable_encoder(obj_in)
    #     obj_in_data
    
    
    
    
    
    async def authenticate(self, db:AsyncSession,username: str, password:str )-> User | None:
        user_obj = await self.get_by_username(db, username=username)
        if not user_obj:
            return None
        
        
    
    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser
    
    
    
user = CRUDUser(User)