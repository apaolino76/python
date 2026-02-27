from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from models.vwestatistica_avaliacao_model import VwEstatisticaAvaliacoesModel
from schemas.vwestatistica_avaliacao_schema import VwEstisticaAvaliacaoSchema
from core.deps import get_session_JEDi, get_current_user
from api.v1.endpoints.utils.utils import transforma_schema_data_frame

router = APIRouter()

# GET Estatísticas por Avaliação
@router.get('/avaliacoes', status_code=status.HTTP_200_OK, response_model=VwEstisticaAvaliacaoSchema)
async def get_avaliacoes(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session_JEDi)):
    try:
        async with db as session:
            query = select(VwEstatisticaAvaliacoesModel)
            result = await session.execute(query)
            data: List[VwEstisticaAvaliacaoSchema] = result.scalars().unique().all()
            
        df = await transforma_schema_data_frame(data)
        
        # Transformar o DataFrame para formato longo (long-form) para usar no seaborn
        df_long = pd.melt(
            df,
            id_vars='avaliacao',
            value_vars=['autoavaliacao', 'avaliacao_jogo'],
            var_name='Fonte',
            value_name='Percentual de Acertos'
        )

        # Criar o gráfico de barras com seaborn
        plt.figure(figsize=(10, 6))
        sns.set(style="whitegrid")

        grafico = sns.barplot(
            data=df_long,
            x='avaliacao',
            y='Percentual de Acertos',
            hue='Fonte',
            palette=['royalblue', 'darkorange']
        )

        # Ajustes estéticos
        plt.title('Percentual de Acertos por Avaliação (Autoavaliação vs Avaliação do Jogo)')
        plt.xlabel('Avaliação')
        plt.ylabel('Percentual de Acertos (%)')
        plt.ylim(0, 100)
        plt.xticks(rotation=45)
        plt.legend(title='Fonte')
        plt.tight_layout()

        # Exibir o gráfico
        plt.show()

            
        return {
            "total_regras": len(regras),
            "links_imagens": links_imagens,
            "regras": regras
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

