from typing import Optional, Any
from pydantic import BaseModel
from decimal import Decimal

class RespostaMetricasSchema(BaseModel):

    id: Optional[int] = None
    texto: str
    publico_infantil: Decimal
    publicio_adulto: Decimal

