from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import pandas as pd
import numpy as np 
from mlxtend.frequent_patterns import apriori, association_rules

from models.usuario_model import UsuarioModel
from models.vwapriori_model import VwAprioriModel
from schemas.vwapriori_schema import VwAprioriSchema, RespostaApriorSchema
from core.deps import get_session_JEDi, get_current_user
from api.v1.endpoints.regras.utils import transforma_schema_data_frame, colunas_desejadas, discretizar_coluna, gerar_graficos_e_regras

router = APIRouter()

# GET Logado
@router.get('/', status_code=status.HTTP_200_OK, response_model=RespostaApriorSchema)
async def get_rules(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session_JEDi)):
    try:
        async with db as session:
            query = select(VwAprioriModel)
            result = await session.execute(query)
            data: List[VwAprioriSchema] = result.scalars().unique().all()
            
        df = await transforma_schema_data_frame(data)
        #print(df.head())
            
        # Discretização e Seleção de Colunas
        df_discre = await discretizar_coluna(df, 'idade', [0, 18, 35, 60, 100], ['adolescente', 'jovem', 'adulto', 'idoso'])
            
        df_onehot = pd.get_dummies(df_discre[colunas_desejadas])
        
        # Apriori
        frequent_itemsets = apriori(df_onehot, min_support=0.05, use_colnames=True)
        with np.errstate(divide='ignore', invalid='ignore'):
            rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.75)

        if rules.empty:
            raise HTTPException(detail='Nenhuma regra encontrada para os parâmetros atuais...', status_code=status.HTTP_404_NOT_FOUND)
        
        regras, links_imagens = await gerar_graficos_e_regras(rules)

        return {
            "total_regras": len(regras),
            "links_imagens": links_imagens,
            "regras": regras
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
