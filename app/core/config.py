from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_NAME: str = Field(..., env="DB_NAME")

    DB_POOL_MIN_SIZE: int = Field(1, env="DB_POOL_MIN_SIZE")
    DB_POOL_MAX_SIZE: int = Field(10, env="DB_POOL_MAX_SIZE")

    API_PREFIX: str = Field(..., env="API_PREFIX")

    class Config:
        env_file = ".env"


settings = Settings()
