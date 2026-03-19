from api.v1.endpoints.utils.utils import (
    transforma_em_dataframe,
    gerar_grafico_avaliacoes, 
    gerar_grafico_categoria_turma, 
    gerar_grafico_partida_escola, 
    gerar_grafico_perfil_noticia
)

class GraficosService:
    
    @staticmethod
    async def criar_grafico_avaliacao(data, path: str):
        # Aqui você centraliza qualquer lógica extra antes de gerar a imagem
        df = await transforma_em_dataframe(data)
        return await gerar_grafico_avaliacoes(df, path)

    @staticmethod
    async def criar_grafico_categoria(data, path: str):
        df = await transforma_em_dataframe(data)
        return await gerar_grafico_categoria_turma(df, path)

    @staticmethod
    async def criar_grafico_partida(data, path: str):
        df = await transforma_em_dataframe(data)
        return await gerar_grafico_partida_escola(df, path)

    @staticmethod
    async def criar_grafico_perfil(data, path: str):
        df = await transforma_em_dataframe(data)
        return await gerar_grafico_perfil_noticia(df, path)