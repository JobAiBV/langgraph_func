from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    swagger_html_file: str = "files/swagger.html"
    json_route: str = "openapi.json" # if changed also change the swagger_html_file