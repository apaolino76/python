from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from models.vwestatistica_avaliacao_model import VwEstatisticaAvaliacoesModel
from schemas.estatisticas_schema import EstisticaAvaliacaoSchema
from core.deps import get_session_JEDi, get_current_user
from api.v1.endpoints.utils.utils import transforma_dados_avaliacao, gerar_grafico_avaliacoes

router = APIRouter()

# GET Estatísticas por Avaliação
@router.get('/avaliacoes', status_code=status.HTTP_200_OK)
async def get_avaliacoes(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session_JEDi)):
    try:
        async with db as session:
            query = select(VwEstatisticaAvaliacoesModel)
            result = await session.execute(query)
            data: List[EstisticaAvaliacaoSchema] = result.scalars().all()

        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        df = await transforma_dados_avaliacao(data)

        dados, links_imagens = await gerar_grafico_avaliacoes(df)

        return {
            "dados": dados,
            "links_graficos": links_imagens
        }

            
        '''       
        if hasattr(df, 'to_dict'):
            return df.to_dict(orient="records")

        return dados
               
        return {
            "total_regras": len(regras),
            "links_imagens": links_imagens,
            "regras": regras
        }
        '''
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

