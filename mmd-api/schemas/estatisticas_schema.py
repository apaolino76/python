from typing import Optional, List, Dict
from pydantic import BaseModel
from decimal import Decimal

class EstisticaAvaliacaoSchema(BaseModel):
        
    id: Optional[int] = None
    avaliacao: str
    autoavaliacao: Decimal
    avaliacao_jogo: Decimal
'''
class RespostaApriorSchema(BaseModel):
    total_regras: int
    links_imagens: Dict[str, str]
    regras: List[RegrasAssociacaoSchema]
'''
