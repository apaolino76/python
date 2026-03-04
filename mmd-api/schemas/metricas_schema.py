from typing import Optional, Any
from pydantic import BaseModel
from decimal import Decimal

class RespostaMetricasSchema(BaseModel):

    id: Optional[int] = None
    texto: str
    publico_infantil: Decimal
    publico_adulto: Decimal

