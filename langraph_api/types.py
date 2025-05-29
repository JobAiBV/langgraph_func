from typing import TypeVar
from pydantic import BaseModel


TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)