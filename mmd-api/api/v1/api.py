from fastapi import APIRouter
from api.v1.endpoints import usuario
from api.v1.endpoints import regra
from api.v1.endpoints import estatisticas

api_router = APIRouter()

api_router.include_router(usuario.router, prefix='/usuarios', tags=["Usuários"])
api_router.include_router(regra.router, prefix='/regras', tags=["Mineração de Dados"])
api_router.include_router(estatisticas.router, prefix='/estatisticas', tags=["Estatísticas"])

