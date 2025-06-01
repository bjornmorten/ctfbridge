"""Base models for CTFd API responses"""

from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class CTFdResponse(BaseModel, Generic[T]):
    """Base model for CTFd API responses"""

    success: bool = True
    data: T


class CTFdErrorResponse(BaseModel):
    """Model for CTFd API error responses"""

    success: bool = False
    message: str
