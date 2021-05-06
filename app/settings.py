from typing import List

from pydantic import BaseSettings, Field, RedisDsn


class Settings(BaseSettings):
    REDIS_URL: RedisDsn = Field('redis://localhost:6379/0', env='REDIS_URL')
    IMAGE_SIZES: List[int] = [32, 64]


settings = Settings()
