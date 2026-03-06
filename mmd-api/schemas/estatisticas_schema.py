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

class EstatisticaCategoriaTurmaSchema(BaseModel):

    id: Optional[int] = None
    escola: Optional[str]
    turma: str
    categoria: str
    media_acertos: Decimal
    media_erros: Decimal

class EstatisticaPartidaTurmaSchema(BaseModel):

    id: Optional[int] = None
    escola: str
    turma: str
    PI: Decimal
    PF: Decimal

class RespostaEstatisticaSchema(BaseModel):
    total: int
    link_imagem: Dict[str, str]
    dados: List[Dict[str, Any]]
