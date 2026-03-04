import math
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
# from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session_JEDi, get_current_user
from core.configs import settings
from models.usuario_model import UsuarioModel
from schemas.metricas_schema import RespostaMetricasSchema

router = APIRouter()

# POST Calcular Tempo de Leitura
@router.post(
    '/tempo_leitura',
    status_code=status.HTTP_200_OK,
    response_model=RespostaMetricasSchema,
)
async def post_tempo_leitura(
    texto: str,
    perguntas_tecnicas: bool = False,
    possui_img: bool = False,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    """
    Calcula o tempo estimado de leitura em segundos.
    :param texto: A pergunta ou frase a ser lida.
    :return: Tempo em segundos.
    """
    try:
        # 1. Conta o número de palavras
        palavras = texto.split()
        total_palavras = len(palavras)
        
        # 2. Calcula o tempo em minutos
        tp_infant_min = total_palavras / settings.WPM_INFANTIL
        to_adulto_min = total_palavras / settings.WPM_ADULTO
        
        # 3. Converte para segundos
        tp_infant_seg = tp_infant_min * 60
        tp_adulto_seg = to_adulto_min * 60
        
        # Adicionamos um "tempo de reação" fixo (ex: 1.5s) para o cérebro 
        # processar o início e o fim da leitura.
        tp_total_infant = tp_infant_seg + 1.5
        tp_total_adulto = tp_adulto_seg + 1.5
        
        # Se a pergunta for técnica: Adicione um multiplicador de dificuldade (ex: tempo X 1.2)
        if perguntas_tecnicas:
            tp_total_infant *= 1.2
            tp_total_adulto *= 1.2

        # Se a pergunta tiver uma imagem: some de 3 a 5 segundos fixos
        if possui_img:
            tp_total_infant += settings.WPM_IMAGEM
            tp_total_adulto += settings.WPM_IMAGEM
        
        return {
            "texto": texto,
            "publico_infantil":  math.ceil(tp_total_infant),
            "publico_adulto":  math.ceil(tp_total_adulto),
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
