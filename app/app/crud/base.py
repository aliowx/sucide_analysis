from datetime import datetime
from typing import Any, Generic, Sequence, Type, TypeVar, Union, List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import  Row, RowMapping, and_, exc, func, select, update

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)




class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType])-> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        
        
    async def get(
        self,
        db: AsyncSession,
        id_: int | str   
    )-> ModelType | None:
        query = select(self.model).where(
        and_(
            self.model.id == id_,
            self.model.is_deleted.is_(None) 
        )
    )
        response = await db.execute(query)
        return response.scalar_one_or_none
    
    async def get_by_ids(
        self,
        db: AsyncSession,
        list_ids: list[int | str]
    )-> Sequence[Row | RowMapping | Any]:
        query = select(self.model).where(
            and_(
                self.model.id.in_(list_ids),
                self.model.is_deleted.is_(None)
            )
        )
        response = await db.execute(query)
        return response.scalars().all()
    
    async def get_count(
        self,
        db: AsyncSession
    )-> ModelType | None:
        query = select(
            func.count()).select_from(select(self.model).subquery()
        )
        response = await db.execute(query)
        return response.scalar_one() 
    
    
    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int | None = 100,
        order_by: list = None,
        order_field: str = "created",
        order_desc: bool = False
    )-> Sequence[Union[Row, RowMapping, Any]]:
        if order_by is None:
            order_by = []
        
        
        if order_desc:
            order_by.append(getattr(self.model, order_field).desc())
        else:
             order_by.append(getattr(self.model, order_field).asc())  
             
        query = (
            select(
                self.model
            ).where(
                self.model.is_deleted.is_(None)
            ).order_by(
                *order_by
            ).offset(
                skip
            )
        )
        
        if limit is not None:
            query = query.limit(limit)
            
        response = await db.execute(query)
        return response.scalar().all() 