from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.negocio.perguntas import PerguntasModel
from models.negocio.tema import TemaModel
from models.negocio.area import AreaModel
from models.negocio.categoria import CategoriaModel
from models.negocio.perguntas_categorias import PerguntasCategoriasModel

class NuvemPalavrasRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_perguntas_para_nuvem(self, filters):
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

        # Aplicação dos filtros
        if filters.area:
            query = query.where(AreaModel.id == filters.area)
        if filters.tema:
            query = query.where(TemaModel.nome == filters.tema)
        if filters.categoria:
            query = query.where(CategoriaModel.descricao == filters.categoria)
        if filters.respcerta:
            query = query.where(PerguntasModel.respcerta == filters.respcerta)

        result = await self.db.execute(query)
        
        return result.all()