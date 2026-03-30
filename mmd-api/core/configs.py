from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    '''
    Configurações gerais usadas na aplicação    
    '''
    DB_USER_API: str
    DB_PASS_API: str
    DB_HOST_API: str
    DB_PORT_API: int
    DB_NAME_API: str

    DB_USER_JEDI: str
    DB_PASS_JEDI: str
    DB_HOST_JEDI: str
    DB_PORT_JEDI: int
    DB_NAME_JEDI: str

    # Montagem dinâmica das URLs
    @property
    def DB_URL_API(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER_API}:{self.DB_PASS_API}@{self.DB_HOST_API}:{self.DB_PORT_API}/{self.DB_NAME_API}"
    
    @property
    def DB_URL_JEDI(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER_JEDI}:{self.DB_PASS_JEDI}@{self.DB_HOST_JEDI}:{self.DB_PORT_JEDI}/{self.DB_NAME_JEDI}"

    API_V1_STR: str

    DBBaseModel: ClassVar = declarative_base()
    DBBaseModelJEDi: ClassVar = declarative_base()

    JWT_SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    WPM_INFANTIL: int
    WPM_ADULTO: int
    WPM_IMAGEM: int
    
    # Configuração para ler o arquivo .env
    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=True
    )

settings = Settings()