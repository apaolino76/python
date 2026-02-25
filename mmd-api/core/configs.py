from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    '''
    Configurações gerais usadas na aplicação    
    '''

    API_V1_STR: str = '/api/v1'
    DB_URL: str = "mysql+aiomysql://root:@localhost:3306/fastapi"
    DBBaseModel: ClassVar = declarative_base()

    JWT_SECRET: str = 'pZ51QzZaNystmR1-DG37rFzrpsGkU75gAHrdkDmXAZ8'
    ALGORITHM: str = 'HS256'
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitiva = True

settings: Settings = Settings()
