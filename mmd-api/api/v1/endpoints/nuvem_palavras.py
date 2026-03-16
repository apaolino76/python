
import time
import matplotlib.pyplot as plt
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import spacy
'''
import nltk
from nltk.corpus import stopwords
'''
from wordcloud import WordCloud

from models.usuario_model import UsuarioModel
from models.negocio.perguntas import PerguntasModel
from models.negocio.tema import TemaModel
from models.negocio.area import AreaModel
from models.negocio.categoria import CategoriaModel
from models.negocio.perguntas_categorias import PerguntasCategoriasModel
from schemas.nuvem_palavras_schema import NuvemFilterSchema, NuvemPalavraSchema
from core.deps import get_session_JEDi, get_current_user
from api.v1.endpoints.utils.utils import gerar_nuvem_palavras 

router = APIRouter(redirect_slashes=False)

# GET Regras
@router.get('', status_code=status.HTTP_200_OK, response_model=NuvemPalavraSchema)
async def get_palavras(
    request: Request,
    filters: NuvemFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        async with db as session:
            query = (select(
                PerguntasModel.id,
                PerguntasModel.pergunta,
                PerguntasModel.respcerta,
                TemaModel.nome.label('tema'),
                AreaModel.descricao.label('area'),
                CategoriaModel.descricao.label('categoria')
            )
            .join(TemaModel, PerguntasModel.id_tema == TemaModel.id)
            .join(AreaModel, TemaModel.id_area == AreaModel.id)
            .join(PerguntasCategoriasModel, PerguntasModel.id == PerguntasCategoriasModel.id_pergunta)
            .join(CategoriaModel, PerguntasCategoriasModel.id_categoria == CategoriaModel.id))
            if filters.area:
                query = query.where(AreaModel.id == filters.area)
            if filters.tema:
                query = query.where(TemaModel.nome == filters.tema)
            if filters.categoria:
                query = query.where(CategoriaModel.descricao == filters.categoria)
            if filters.respcerta:
                query = query.where(PerguntasModel.respcerta == filters.respcerta)
            result = await session.execute(query)
            registros = result.all()
        
        if len(registros) == 0:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)

        # Unificando tudo em um único texto
        texto_completo = " ".join([reg.pergunta for reg in registros])

        '''
        # Baixar a lista de stopwords do NLTK
        nltk.download('stopwords')
        stop_words_pt = set(stopwords.words('portuguese'))
        
        # Configurando Stopwords em Português
        palavras_extras = {"de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "na", "no", "os", "as", "ao", "se", "sobre", "diz", "faz", "deve", "pode"}
        # Você pode somar as stopwords padrão da biblioteca se desejar
        stop_words_pt.update(palavras_extras)        
        '''
        # Carregar o modelo de português do spaCy
        nlp = spacy.load("pt_core_news_sm")

        # Processar o texto com spaCy
        doc = nlp(texto_completo.lower())

        # Filtrar e Lematizar
        # Manter apenas substantivos, adjetivos e verbos, removendo stop words, pontuação e pronomes.
        palavras_limpas = []
        for token in doc:
            if not token.is_stop and not token.is_punct and not token.is_space:
                # Adicionamos o lemma (raiz da palavra) para agrupar variações
                palavras_limpas.append(token.lemma_)
        
        # Transformar a lista de volta em uma string única
        texto_final = " ".join(palavras_limpas)

        # Criando a nuvem de palavras
        nuvem = WordCloud(
            width=800, 
            height=400,
            background_color='white',
            # stopwords=stop_words_pt,
            colormap='viridis', # Esquema de cores
            max_words=100,
            min_font_size=10
        ).generate(texto_final)

        await gerar_nuvem_palavras(nuvem)

        base_url = str(request.base_url)
        print(base_url)
        timestamp = int(time.time())
        link = {
            "link": f"{base_url}static/nuvem_palavaras/img/nuvem_palavras.png?v={timestamp}"
        }

        return {
            "total_registros": len(registros),
            "dados": registros,
            "texto_completo": texto_completo,
            "link_grafico": link 
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
'''


'''        
