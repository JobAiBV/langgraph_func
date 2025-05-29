import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    function_base_url: str = os.getenv("FUNCTION_BASE_URL")