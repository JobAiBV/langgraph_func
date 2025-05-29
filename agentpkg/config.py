# config.py
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, HttpUrl
from typing import Literal, Optional
import azure.functions as func

class Settings(BaseSettings):
    function_base_url: str = Field(..., alias="FUNCTIONS_BASE_URL")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    # Log level as usual
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field("INFO", alias="LOG_LEVEL")

    # Auth level choices (maps to func.AuthLevel enum)
    auth_mode: Literal[
        "anonymous", "function", "admin"
    ] = Field(..., alias="AUTH_MODE")

    class Config:
        env_file = None
        populate_by_name = True

    @field_validator("log_level", mode="before")
    def normalize_log_level(cls, v: str) -> str:
        return v.upper()

    def get_auth_level(self) -> func.AuthLevel:
        """Maps the string auth_mode to a func.AuthLevel enum."""
        return {
            "anonymous": func.AuthLevel.ANONYMOUS,
            "function": func.AuthLevel.FUNCTION,
            "admin": func.AuthLevel.ADMIN
        }[self.auth_mode]
