import logging
import heapq
import numpy as np
import math
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app import crud, schemas
from app.core.config import settings

logger = logging.getLogger(__name__)


# async def create_super_admin(db: AsyncSession)-> None:
#     user = await 
