import matplotlib
matplotlib.use('Agg') # Força o backend não-interativo ANTES do pyplot
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Any
from fastapi import HTTPException,status
import pandas as pd

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


async def gerar_graficos_e_regras(regras: pd.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    try:
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
        plt.close('all')

        # Preparar JSON
        rules_list = regras[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()
        rules_list['antecedents'] = rules_list['antecedents'].apply(list)
        rules_list['consequents'] = rules_list['consequents'].apply(list)
        
        return rules_list.to_dict(orient='records'),{
            "grafico_lift": "static/regras/img/top10_lift.png",
            "grafico_dispersao": "static/regras/img/dispersao.png"
        }
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Regras: {e}")


# async def gerar_grafico_avaliacoes(dados: pd.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
async def gerar_grafico_avaliacoes(dados: pd.DataFrame):
    try:        
        # Transformar o DataFrame para formato longo (long-form) para usar no seaborn
        df_long = pd.melt(
            dados,
            id_vars='avaliacao',
            value_vars=['autoavaliacao', 'avaliacao_jogo'],
            var_name='fonte',
            value_name='percentual_acertos'
        )

        # Criar o gráfico de barras com seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=df_long,
            x='avaliacao',
            y='percentual_acertos',
            hue='fonte',
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
        plt.close('all')
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Avaliações: {e}")

async def gerar_grafico_categoria_turma(dados: pd.DataFrame):
    try:
        # Transformar para formato longo
        df_meltado = dados.melt(
            id_vars=['categoria', 'turma'],
            value_vars=['media_acertos', 'media_erros'],
            var_name='Tipo',
            value_name='Média'
        )
        
        # 2. Normalização dos nomes para bater com a 'ordem'
        # Transformamos 'media_acertos' em 'acerto' e 'media_erros' em 'erro'        
        df_meltado['Tipo'] = df_meltado['Tipo'].replace({
            'media_acertos': 'acerto', 
            'media_erros': 'erro'
        })

        # Criar coluna combinando tipo e turma para o eixo X
        df_meltado['Tipo_Turma'] = df_meltado['Tipo'] + ' - ' + df_meltado['turma']

        # Definir ordem personalizada
        ordem = ['acerto - Turma A', 'erro - Turma A', 'acerto - Turma B', 'erro - Turma B', 'acerto - Turma C', 'erro - Turma C']   

        # Criar o gráfico de barras com seaborn
        plt.figure(figsize=(10, 6))

        grafico = sns.barplot(
            data=df_meltado,
            x='Tipo_Turma',
            y='Média',
            hue='categoria',
            order=ordem,
            palette='Set2')
        
        # Adiciona os valores nas barras
        for barra in grafico.patches:
            altura = barra.get_height()
            if altura > 0:
                grafico.annotate(
                    f'{altura:.0f}%',
                    (barra.get_x() + barra.get_width() / 2, altura),
                    ha='center',
                    va='bottom',
                    fontsize=9
                )
            
        # Ajustes finais
        plt.title('Percentual de Acerto/Erro por Turma e Categoria', fontsize=14)
        plt.xlabel('Tipo de Resposta por Turma')
        plt.ylabel('Média')
        plt.ylim(0, 100)
        plt.legend(title='Categoria')
        plt.tight_layout()

        path_avaliacao = "static/estatisticas/img/categoria_turma.png"
        plt.savefig(path_avaliacao)
        # Importante: Libera memória
        plt.close('all')
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Categorias: {e}") 

async def gerar_grafico_partida_escola(dados: pd.DataFrame):
    try:
        # Transformar para formato longo
        df_meltado = dados.melt(
            id_vars=['escola', 'turma'],
            value_vars=['PI', 'PF'],
            var_name='Tipo',
            value_name='Média'
        )
        
        # Criar coluna combinando tipo e turma para o eixo X
        df_meltado['Tipo_Turma'] = df_meltado['Tipo'] + ' - ' + df_meltado['turma']

        # Definir ordem personalizada
        ordem = ['PI - Turma A', 'PF - Turma A', 'PI - Turma B', 'PF - Turma B', 'PI - Turma C', 'PF - Turma C']

        # Criar o gráfico de barras com seaborn
        plt.figure(figsize=(10, 6))

        grafico = sns.barplot(
            data=df_meltado,
            x='Tipo_Turma',
            y='Média',
            hue='escola',
            order=ordem,
            palette=['royalblue', 'darkorange']
        )
        
        # Adiciona os valores nas barras
        for barra in grafico.patches:
            altura = barra.get_height()
            if altura > 0:
                grafico.annotate(
                    f'{altura:.0f}%',
                    (barra.get_x() + barra.get_width() / 2, altura),
                    ha='center',
                    va='bottom',
                    fontsize=9
                )
            
        # Ajustes finais
        plt.title('Percentual de Acertos por Tipo da Partida e Turma', fontsize=14)
        plt.xlabel('Desempenho por Tipo da Partida e Turma')
        plt.ylabel('Média')
        plt.ylim(0, 100)
        plt.legend(title='escola')
        plt.tight_layout()

        path_avaliacao = "static/estatisticas/img/escola_turma.png"
        plt.savefig(path_avaliacao)
        # Importante: Libera memória
        plt.close('all')
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Partidas: {e}") 
