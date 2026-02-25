from fastapi import APIRouter
from api.v1.endpoints import artigo
from api.v1.endpoints import usuario
from api.v1.endpoints import regras

api_router = APIRouter()
api_router.include_router(artigo.router, prefix='/artigos', tags=["Artigos"])
api_router.include_router(usuario.router, prefix='/usuarios', tags=["Usuários"])
api_router.include_router(regras.router, prefix='/rules', tags=["Mineração de Dados"])