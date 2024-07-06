from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

load_dotenv()

class Settings(BaseSettings):
    UPSTAGE_API_KEY:str=""
    TAVILY_API_KEY:str=""
    NEWS_API_KEY:str=""
    DB_USER:str=""
    DB_PASSWORD:str=""
    DSN:str=""
    
    class Config:
        env_file = ".env"



@lru_cache()
def get_setting():
    return Settings()