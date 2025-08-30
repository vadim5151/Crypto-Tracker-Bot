import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict



load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
