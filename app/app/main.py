from contextlib import asynccontextmanager
import logging, sys, os

from fastapi import FastAPI, Request, Response
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.middleware.cors import  CORSMiddleware
from app.core.config import settings
from app.core.middleware.time_logger import TimeLoggerMiddleware
from cache import Cache



def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(levelname)s:%(asctime)s %(name)s:%(funcName)s:%(lineno)s %(message)s" 
                   
        )
    )
    logger.addHandler(handler)
    

init_logger()



def make_middleware(
    
)-> list[Middleware]:
    middleware = []
    if settings.DEBUG:
        middleware.append(Middleware(TimeLoggerMiddleware))
    return middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_cache = Cache()
    url = str(settings.REDIS_URI)
    await redis_cache.init(
        host_url=url,
        prefix='api_cache',
        response_header="X-API-Cache",
        ignore_arg_types=[Request, Response, Session, AsyncSession,] 
    )
    yield
    
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    middleware=make_middleware(),
)

if settings.SUB_PATH:
    app.mount(f"{settings.SUB_PATH}", app)
    
    
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],        
    )
    

app.mount("/static", StaticFiles(directory="app/static"), name="static")
