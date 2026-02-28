from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from decimal import Decimal

class EstisticaAvaliacaoSchema(BaseModel):
        
    id: Optional[int] = None
    avaliacao: str
    fonte: str
    percentual_acertos: Decimal

class RespostaEstatisticaAvaliacaoSchema(BaseModel):
    total: int
    link_imagem: Dict[str, str]
    dados: List[Dict[str, Any]]

