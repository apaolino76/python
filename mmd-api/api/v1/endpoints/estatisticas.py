from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Request, BackgroundTasks
# from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from models.vwestatistica_avaliacao_model import VwEstatisticaAvaliacoesModel
from models.vwestatistica_categoria_turma_model import VwEstatisticaCategoriaTurmaModel
from models.vwestatististica_partida_turma import VwEstatisticaPartidaTurmaModel
from schemas.estatisticas_schema import RespostaEstatisticaSchema
from core.deps import get_session_JEDi, get_current_user
from api.v1.endpoints.utils.utils import transforma_em_dataframe, gerar_grafico_avaliacoes, gerar_grafico_categoria_turma, gerar_grafico_partida_escola

router = APIRouter()

# GET Estatísticas por Avaliação
@router.get('/avaliacao', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
# @cache(expire=300) # Cache de 5 minutos
async def get_avaliacoes(
    request: Request,
    background_tasks: BackgroundTasks,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        async with db as session:
            query = select(VwEstatisticaAvaliacoesModel)
            result = await session.execute(query)
            data = result.scalars().all()

        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        df = await transforma_em_dataframe(data)

        # 1. Agendamos a geração da imagem para depois da resposta
        background_tasks.add_task(gerar_grafico_avaliacoes, df)

        # 2. Construímos a URL da imagem
        base_url = str(request.base_url)
        link = {"grafico_avaliacao": f"{base_url}static/estatisticas/img/acertos_avaliacao.png"}

        return {
            "total": len(df),
            "link_imagem": link,
            "dados": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    
    
# GET Estatísticas por Categoria e Turma
@router.get('/categoria_turma', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
# @cache(expire=300) # Cache de 5 minutos
async def get_categoria_turma(
    request: Request,
    background_tasks: BackgroundTasks,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        async with db as session:
            query = select(VwEstatisticaCategoriaTurmaModel)
            result = await session.execute(query)
            data = result.scalars().all()
        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        df = await transforma_em_dataframe(data)

        # 1. Agendamos a geração da imagem para depois da resposta
        background_tasks.add_task(gerar_grafico_categoria_turma, df)
        
        # 2. Construímos a URL da imagem
        base_url = str(request.base_url)
        link = {"grafico_categoria_turma": f"{base_url}static/estatisticas/img/categoria_turma.png"}

        return {
            "total": len(df),
            "link_imagem": link,
            "dados": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    

# GET Estatísticas por Escola e Partida
@router.get('/partida_escola', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
# @cache(expire=300) # Cache de 5 minutos
async def get_partida_escola(
    request: Request,
    background_tasks: BackgroundTasks,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        async with db as session:
            query = select(VwEstatisticaPartidaTurmaModel)
            result = await session.execute(query)
            data = result.scalars().all()
        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        df = await transforma_em_dataframe(data)

        # 1. Agendamos a geração da imagem para depois da resposta
        background_tasks.add_task(gerar_grafico_partida_escola, df)
        
        # 2. Construímos a URL da imagem
        base_url = str(request.base_url)
        link = {"grafico_escola_turma": f"{base_url}static/estatisticas/img/escola_turma.png"}

        return {
            "total": len(df),
            "link_imagem": link,
            "dados": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    

