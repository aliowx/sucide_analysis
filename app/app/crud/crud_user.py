from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, select

from sqlalchemy.ext.asyncio import AsyncSession

class CRUDUser():
    ...