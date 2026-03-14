
import time
import matplotlib.pyplot as plt
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from wordcloud import WordCloud, STOPWORDS

from models.usuario_model import UsuarioModel
from models.perguntas import PerguntasModel
from schemas.nuvem_palavras_schema import NuvemPalavraSchema
from core.deps import get_session_JEDi, get_current_user
from api.v1.endpoints.utils.utils import gerar_nuvem_palavras 

router = APIRouter(redirect_slashes=False)

# GET Regras
@router.get('', status_code=status.HTTP_200_OK, response_model=NuvemPalavraSchema)
async def get_palavaras(request: Request, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session_JEDi)):
    try:
        async with db as session:
            query = select(PerguntasModel.pergunta)
            result = await session.execute(query)
            perguntas = result.scalars().all()
        
        # Unificando tudo em um único texto
        texto_completo = " ".join(perguntas)

        # Configurando Stopwords em Português
        stopwords_pt = set(["de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "na", "no", "os", "as"])
        # Você pode somar as stopwords padrão da biblioteca se desejar
        stopwords_pt.update(STOPWORDS)

        # Criando a nuvem de palavras
        nuvem = WordCloud(
            width=800, 
            height=400,
            background_color='white',
            stopwords=stopwords_pt,
            colormap='viridis', # Esquema de cores
            min_font_size=10
        ).generate(texto_completo)

        await gerar_nuvem_palavras(nuvem)

        base_url = str(request.base_url)
        print(base_url)
        timestamp = int(time.time())
        link = {
            "link": f"{base_url}static/nuvem_palavaras/img/nuvem_palavras.png?v={timestamp}"
        }

        return {
            "perguntas": texto_completo,
            "link_grafico": link
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
