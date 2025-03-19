from contextlib import asynccontextmanager
import logging, sys, os

from fastapi import FastAPI, Request, Response
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.middleware.cors import  CORSMiddleware

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