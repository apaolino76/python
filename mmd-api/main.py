from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router
import uvicorn

app = FastAPI(
    title='JEDi Educa - API para Mineração de Dados',
    version='0.0.1',
    description='Uma API inteligente para análise de dados oriundos do JEDI Educa. '
)
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)

'''
Token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzcyNTgzNzk3LCJpYXQiOjE3NzE5Nzg5OTcsInN1YiI6IjMifQ.NEbUaHH0XOnZMAco040MS00IU3ZQXQ878E0recr-7y0
Type = bearer
'''