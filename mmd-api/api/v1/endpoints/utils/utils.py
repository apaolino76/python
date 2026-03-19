from typing import List, Dict, Tuple, Any
from api.v1.endpoints.utils.ChartGenerator import chart_tool
import pandas as pd
import textwrap

colunas_desejadas = [
    'escola',
    'turma',
    'fx_idade',
    'categoria',
    'auto_avaliacao',
    'avaliacao_jogo',
    'capacidade_critica'
]

async def transforma_em_dataframe(lista_modelos: List[Any]) -> pd.DataFrame:
    try:
        """
        Converte uma lista de modelos (Pydantic ou SQLAlchemy) em DataFrame,
        removendo metadados internos do SQLAlchemy.
        """
        if not lista_modelos:
            return pd.DataFrame()

        data = []
        for item in lista_modelos:
            # Se for Pydantic (V2)
            if hasattr(item, 'model_dump'):
                data.append(item.model_dump())
            # Se for Pydantic (V1)
            elif hasattr(item, 'dict'):
                data.append(item.dict())
            # Se for um modelo SQLAlchemy
            else:
                d = dict(vars(item))
                d.pop('_sa_instance_state', None) # Remove o erro de serialização
                data.append(d)
        
        return pd.DataFrame.from_records(data)
    except Exception as e:
        print(f"Erro durante o processo de transformação do DataFrame: {e}")
        raise e

async def discretizar_coluna(df: pd.DataFrame, campo: str, bins: List[int], rotulos: List[str]) -> pd.DataFrame:
    try:
        """
        Discretiza uma coluna numérica em categorias (bins).
        
        :param df: O DataFrame original.
        :param campo: O nome da coluna (ex: 'idade').
        :param bins: Lista de limites (ex: [0, 18, 35, 60, 100]).
        :param rotulos: Lista de nomes das faixas (ex: ['adolescente', 'jovem', ...]).
        :return: DataFrame com a nova coluna adicionada.
        """
        nome_nova_coluna = f"fx_{campo}"
        
        # Executa a discretização
        df[nome_nova_coluna] = pd.cut(
            df[campo],
            bins=bins,
            labels=rotulos
        )
        
        return df
    except Exception as e:
        print(f"Erro durante o processo de discretização da coluna: {e}")
        raise e


# def limpar_nome(item_set):
#     # Remove prefixos comuns gerados pelo get_dummies ou discretização
#     substituicoes = ['fx_idade', 'categoria_', 'escola_', 'turma_',  'auto_avaliacao_', 'avaliacao_jogo_', 'capacidade_critica_']
#     nova_lista = []
#     for item in item_set:
#         for s in substituicoes:
#             item = item.replace(s, '')
#         nova_lista.append(item)
#     return nova_lista

def formata_regra_amigavel(row, max_width=40):
    """Limpa frozenset, formata como A -> B e quebra linhas longas."""
    # Remove frozenset({}) e formata
    ant = str(row['antecedents']).replace("frozenset({", "").replace("})", "")
    con = str(row['consequents']).replace("frozenset({", "").replace("})", "")

    # O textwrap.fill quebra o texto se ele passar de 30 caracteres
    ant = textwrap.fill(ant, width=max_width)
    con = textwrap.fill(con, width=max_width)

    return f"{ant}\n→ {con}"
