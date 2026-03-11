from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from decimal import Decimal

class EstisticaAvaliacaoSchema(BaseModel):
        
    id: Optional[int] = None
    escola: Optional[str]
    turma: str
    avaliacao: str
    autoavaliacao: Decimal
    avaliacao_jogo: Decimal

class EstisticaAvaliacaoFilterSchema(BaseModel):
        
    id: Optional[int] = None
    escola: Optional[str] = None
    turma: Optional[str] = None
    avaliacao: Optional[str] = None

class EstatisticaCategoriaTurmaSchema(BaseModel):

    id: Optional[int] = None
    escola: Optional[str]
    turma: str
    categoria: str
    media_acertos: Decimal
    media_erros: Decimal

class EstisticaCategoriaFilterSchema(BaseModel):
        
    id: Optional[int] = None
    escola: Optional[str] = None
    turma: Optional[str] = None
    categoria: Optional[str] = None

class EstatisticaPartidaTurmaSchema(BaseModel):

    id: Optional[int] = None
    escola: str
    turma: str
    PI: Decimal
    PF: Decimal

class EstatisticaPartidaFilterSchema(BaseModel):

    id: Optional[int] = None
    escola: Optional[str] = None
    turma: Optional[str] = None
 
class DistribuicaoNotociaCategoriaSchema(BaseModel):

    id: Optional[int] = None
    categoria: str
    fake_qt: int
    fake_perc: Decimal
    nao_fake_qt: int
    nao_fake_perc: Decimal

class DistribuicaoNotociaCategoriaFilterSchema(BaseModel):

    id: Optional[int] = None
    categoria: Optional[str] = None

class RespostaEstatisticaSchema(BaseModel):
    total: int
    link_imagem: Dict[str, str]
    dados: List[Dict[str, Any]]
