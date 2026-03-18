from typing import List, Dict, Tuple, Any
from fastapi import HTTPException,status
from wordcloud import WordCloud
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

async def gerar_graficos_e_regras(df_regras: pd.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    try:
        # 1. Preparação: Criar a coluna de texto formatada
        df_regras['regra_formatada'] = df_regras.apply(formata_regra_amigavel, axis=1)
        
        # 2. Gerar Gráfico de Dispersão (Todas as Regras)
        path_scatter = "static/regras/img/regras_dispersao.png"
        await chart_tool.plot_scatter(
            df=df_regras,
            path_save=path_scatter,
            params={
                'x': 'support',
                'y': 'confidence',
                'hue': 'lift',
                'size': 'lift',
                'titulo': 'Dispersão das Regras (Suporte vs Confiança)'
            }
        )
        
        # 3. Gerar Gráfico Top 10 (Baseado no Lift)
        df_top10 = df_regras.nlargest(10, 'lift')
        path_top10 = "static/regras/img/regras_top10.png"
        await chart_tool.plot_horizontal_bars(
            df=df_top10,
            path_save=path_top10,
            params={
                'x': 'lift',
                'y': 'regra_formatada',
                'titulo': 'Top 10 Regras por Lift (Força de Associação)',
                'label_x': 'Valor de Lift'
            }
        )

        # Preparar JSON
        rules_list = df_regras[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()
        rules_list['antecedents'] = rules_list['antecedents'].apply(list)
        rules_list['consequents'] = rules_list['consequents'].apply(list)
        
        return rules_list.to_dict(orient='records'),{
            "grafico_lift": path_top10,
            "grafico_dispersao": path_scatter
        }
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Regras: {e}")

async def gerar_grafico_avaliacoes(dados: pd.DataFrame, path_imagem: str):
    try:
        # Preparação (Melt)
        df_long = dados.melt(
            id_vars='avaliacao', 
            value_vars=['autoavaliacao', 'avaliacao_jogo'], 
            var_name='fonte',
            value_name='pct'
        )
    
        # Chamada simplificada
        await chart_tool.plot_barplot(
            df=df_long,
            path_save=path_imagem,
            params={
                'x': 'avaliacao',
                'y': 'pct',
                'hue': 'fonte',
                'titulo': 'Autoavaliação vs Jogo',
                'palette': ['royalblue', 'darkorange'],
                'ylim': 100
            },
            formato_rotulo="{:.1f}%"
        )
    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Avaliações: {e}")

async def gerar_grafico_categoria_turma(dados: pd.DataFrame, path_imagem: str):
    try:
        # 1. Preparação dos dados: Transformação de Wide para Long (Melt)
        # Mapeamos as colunas do banco para nomes amigáveis
        mapping = {'media_acertos': 'Acerto', 'media_erros': 'Erro'}

        # Transformar para formato longo
        df_melt = dados.melt(
            id_vars=['categoria', 'turma'],
            value_vars=['media_acertos', 'media_erros'],
            var_name='Tipo',
            value_name='media'
        )

        # 2. Criar a coluna combinada para o eixo X (ex: "Acerto - Turma A")
        df_melt['Tipo'] = df_melt['Tipo'].replace(mapping)
        df_melt['Legenda_X'] = df_melt['Tipo'] + ' - ' + df_melt['turma']
        
        # 3. Definir a ordem das barras para ficarem agrupadas por turma
        turmas = sorted(dados['turma'].unique())
        ordem_x = []
        for t in turmas:
            ordem_x.extend([f"Acerto - {t}", f"Erro - {t}"])
        
        # 4. Chamar a função mestra da classe
        await chart_tool.plot_barplot(
            df=df_melt,
            path_save=path_imagem,
            params={
                'x': 'Legenda_X',
                'y': 'media',
                'hue': 'categoria',
                'order': ordem_x,
                'titulo': 'Média de Acertos/Erros por Categoria e Turma',
                'label_x': 'Turmas / Tipo',
                'label_y': 'Média (%)',
                'ylim': 100
            },
            formato_rotulo="{:.1f}%"
        )

    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Categorias: {e}") 

async def gerar_grafico_partida_escola(dados: pd.DataFrame, path_imagem: str):
    try:
        # 1. Mapeamento para nomes amigáveis na legenda
        mapping = {'PI': 'Partida Inicial', 'PF': 'Partida Final'}

        # 2. Transformação de Wide para Long
        df_melt = dados.melt(
            id_vars=['escola', 'turma'], 
            value_vars=['PI', 'PF'], 
            var_name='momento', 
            value_name='media'
        )
        
        # Substitui os nomes técnicos pelos nomes do mapping
        df_melt['momento'] = df_melt['momento'].replace(mapping)
        
        # 3. Criar a legenda do eixo X combinando Escola e Turma
        df_melt['eixo_x'] = df_melt['escola'] + " (" + df_melt['turma'] + ")"
        
        # 4. Definir a ordem das barras (Agrupar Pré e Pós por Escola/Turma)
        eixos_unicos = df_melt['eixo_x'].unique()
        ordem_x = sorted(eixos_unicos)

        # 5. Chamada da classe ChartGenerator
        await chart_tool.plot_barplot(
            df=df_melt,
            path_save=path_imagem,
            params={
                'x': 'eixo_x',
                'y': 'media',
                'hue': 'momento', # O que diferencia as cores das barras
                'order': ordem_x,
                'titulo': 'Desempenho Médio: Partida Inicial vs Partida Final',
                'label_x': 'Escola (Turma)',
                'label_y': 'Média de Acertos (%)',
                'ylim': 100,
                'palette': ['#34495e', '#2ecc71'] # Cores customizadas (Cinza e Verde)
            },
            formato_rotulo="{:.1f}%"
        )

    except Exception as e:
        print(f"Erro durante o processo de Gerar Gráfico de Partidas: {e}") 

async def gerar_grafico_perfil_noticia(dados: pd.DataFrame, path_imagem: str):
    try:
        #print(f"Colunas disponíveis: {dados.columns.tolist()}")
        # 1. Preparação: O banco costuma trazer colunas como 'fake' e 'nao_fake'
        # Vamos transformar em formato longo (melt) para o Seaborn colorir por 'Tipo'
        df_melt = dados.melt(
            id_vars=['categoria'], 
            value_vars=['fake_qt', 'nao_fake_qt'], 
            var_name='tipo_noticia', 
            value_name='quantidade'
        )
        
        # 2. Ajuste de nomes para a legenda
        df_melt['tipo_noticia'] = df_melt['tipo_noticia'].replace({
            'fake_qt': 'Fake', 
            'nao_fake_qt': 'Não Fake'
        })

        # 3. Chamada da classe ChartGenerator
        await chart_tool.plot_barplot(
            df=df_melt,
            path_save=path_imagem,
            params={
                'x': 'categoria',
                'y': 'quantidade',
                'hue': 'tipo_noticia',
                'titulo': 'Comparativo: Notícias Fake vs. Não Fake por Categoria',
                'label_x': 'Categorias',
                'label_y': 'Quantidade de Respostas',
                'palette': ['#e74c3c', '#2ecc71'], # Vermelho para Fake, Verde para Não Fake
                'ylim': df_melt['quantidade'].max() # Ajusta o topo com base no maior valor
            },
            formato_rotulo="{:.0f}" # Usamos 0 casas decimais pois é contagem (inteiro)
        )        
    except Exception as e:
        print(f"Erro ao gerar gráfico de perfil: {e}")

async def gerar_nuvem_palavras(nuvem: WordCloud, path_imagem: str):
    try:
        # Apenas delegamos para a classe mestre
        await chart_tool.plot_wordcloud(
            nuvem=nuvem, 
            path_save=path_imagem,
            titulo="Nuvem de Palavras das Questões"
        )        
    except Exception as e:
        print(f"Erro ao gerar gráfico de perfil: {e}")
