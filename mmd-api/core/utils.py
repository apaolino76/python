import pandas as pd
from typing import List
from models.vwapriori_model import VwAprioriModel

colunas_desejadas = [
    'escola',
    'turma',
    'fx_idade',
    'categoria',
    'auto_avaliacao',
    'avaliacao_jogo',
    'capacidade_critica'
]

async def transforma_schema_data_frame(apriori: List[VwAprioriModel]) -> pd.DataFrame:
    """
    Converte uma lista de objetos VwAprioriModel em um DataFrame do Pandas.
    """
    # A lógica de extração permanece eficiente para construção do DataFrame
    data = [
        {
            'id': item.id,
            "origem": item.origem,
            "escola": item.escola,
            "turma": item.turma,
            "login": item.login,
            "jogador": item.jogador,
            "dt_jogo": item.dt_jogo,
            "idade": item.idade,
            "auto_avaliacao": item.auto_avaliacao,
            "avaliacao_jogo": item.avaliacao_jogo,
            "tutor": item.tutor,
            "categoria": item.categoria,
            "tema": item.tema,
            "numero_partidas": item.numero_partidas,
            "tempo_gasto": item.tempo_gasto,
            "percentual_acertos": item.percentual_acertos,
            "percentual_erros": item.percentual_erros,
            "capacidade_critica": item.capacidade_critica
        } for item in apriori
    ]
    
    return pd.DataFrame.from_records(data)

async def discretizar_coluna(
    df: pd.DataFrame, 
    campo: str, 
    bins: List[int], 
    rotulos: List[str]
) -> pd.DataFrame:
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