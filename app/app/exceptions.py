import logging 
import traceback
from typing import Any
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from app.utils import MessageCodes
from app.core.config import settings


logger = logging.getLogger(__name__)


class CustomHTTPException(HTTPException):
    """Custom HTTPException class for common exception handling."""
    
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        msg_code: MessageCodes =  MessageCodes.internal_error,
        detail: str | None = None,
        headers: dict | None = None 
    )-> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.msg_code = msg_code




def get_traceback_info(exc: Exception):
    traceback_str = (traceback.format_tb(exc.__traceback__))[-1]
    traceback_full = "".join(traceback.format_tb(exc.__traceback__))
    exception_type = type(exc).__name__
    return exception_type, traceback_str, traceback_full