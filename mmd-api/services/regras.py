import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from api.v1.endpoints.utils.utils import (
    transforma_em_dataframe, discretizar_coluna, 
    colunas_desejadas, gerar_graficos_e_regras
)

class RegrasService:
    async def processar_regras_associacao(self, data):
        # 1. Transformação inicial
        df = await transforma_em_dataframe(data)
            
        # 2. Engenharia de Recursos (Discretização)
        # Isola a regra de negócio: faixas etárias específicas do seu projeto
        df_discre = await discretizar_coluna(
            df, 'idade', [0, 18, 35, 60, 100], 
            ['adolescente', 'jovem', 'adulto', 'idoso']
        )
            
        # 3. Preparação One-Hot Encoding
        df_onehot = pd.get_dummies(df_discre[colunas_desejadas])
        
        # 4. Execução do Algoritmo Apriori
        frequent_itemsets = apriori(df_onehot, min_support=0.05, use_colnames=True)
        
        with np.errstate(divide='ignore', invalid='ignore'):
            rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.75)

        if rules.empty:
            return None, None
        
        # 5. Geração de saídas (JSON e Imagens)
        regras_json, links_imagens = await gerar_graficos_e_regras(rules)
        return regras_json, links_imagens