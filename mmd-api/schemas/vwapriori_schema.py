from typing import Optional
from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class VwAprioriSchema(BaseModel):
        
    id: Optional[int] = None
    origem: str
    escola: str
    turma: str
    login: str
    jogador: str
    dt_jogo: date
    idade: int
    auto_avaliacao: str
    avaliacao_jogo: str
    tutor: int
    categoria: str
    tema: str
    numero_partidas: int
    tempo_gasto: Decimal
    percentual_acertos: Decimal
    percentual_erros: Decimal
    capacidade_critica: str