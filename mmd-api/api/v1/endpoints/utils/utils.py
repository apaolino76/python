from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt
from models.vwapriori_model import VwAprioriModel
from models.vwestatistica_avaliacao_model import VwEstatisticaAvaliacoesModel
import seaborn as sns

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

async def transforma_dados_avaliacao(avaliacao: List[VwEstatisticaAvaliacoesModel]) -> pd.DataFrame:
    """
    Converte uma lista de objetos VwAprioriModel em um DataFrame do Pandas.
    """
    # A lógica de extração permanece eficiente para construção do DataFrame
    data = [
        {
            "id": item.id,
            "avaliacao": item.avaliacao,
            "autoavaliacao": item.autoavaliacao,
            "avaliacao_jogo": item.avaliacao_jogo
        } for item in avaliacao
    ]
    
    return pd.DataFrame.from_records(data)


async def discretizar_coluna(df: pd.DataFrame, campo: str, bins: List[int], rotulos: List[str]) -> pd.DataFrame:
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

async def gerar_graficos_e_regras(regras: pd.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    # --- Top 10 Lift ---
    rules_plot = regras.sort_values(by='lift', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    plt.barh(range(len(rules_plot)), rules_plot['lift'], color='skyblue')
    plt.yticks(range(len(rules_plot)), [f"{list(a)} => {list(c)}" for a, c in zip(rules_plot['antecedents'], rules_plot['consequents'])])
    plt.xlabel('Lift')
    plt.title('Top 10 Regras por Lift')
    plt.gca().invert_yaxis()
    plt.subplots_adjust(left=0.3)
    path_lift = "static/regras/img/top10_lift.png"
    plt.savefig(path_lift)
    plt.close() # Importante: Libera memória

    # --- Dispersão ---
    plt.figure(figsize=(8, 6))
    plt.scatter(regras['support'], regras['confidence'], alpha=0.7, c=regras['lift'], cmap='viridis')
    plt.xlabel('Support')
    plt.ylabel('Confidence')
    plt.colorbar(label='Lift')
    plt.tight_layout()
    path_scatter = "static/regras/img/dispersao.png"
    plt.savefig(path_scatter)
    plt.close()

    # Preparar JSON
    rules_list = regras[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()
    rules_list['antecedents'] = rules_list['antecedents'].apply(list)
    rules_list['consequents'] = rules_list['consequents'].apply(list)
    
    return rules_list.to_dict(orient='records'),{
        "grafico_lift": "/static/regras/img/top10_lift.png",
        "grafico_dispersao": "/static/regras/img/dispersao.png"
    }

async def gerar_grafico_avaliacoes(dados: pd.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
        
        # Transformar o DataFrame para formato longo (long-form) para usar no seaborn
        df_long = pd.melt(
            dados,
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
        path_avaliacao = "static/estatisticas/img/acertos_avaliacao.png"
        plt.savefig(path_avaliacao)
        # Importante: Libera memória
        plt.close()

        return df_long.to_dict(orient='records'),{
            "grafico_avaliacao": path_avaliacao,
        }
 
