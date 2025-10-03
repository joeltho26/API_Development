from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

# load_dotenv()

class Settings(BaseSettings):
    #database
    database_name: str
    database_user: str
    database_host: str
    database_port: str
    database_password: str
    
    #token
    secret_key: str
    algorithm: str
    access_token_expiration_minutes: int
    
    class Config:
        env_file = ".env"
    
settings = Settings()