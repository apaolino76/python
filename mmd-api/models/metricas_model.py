from sqlalchemy import Column, Integer, String, Numeric
from core.configs import settings
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class MetricasModel(settings.DBBaseModelJEDi):

    id = Column(Integer, primary_key=True)
    texto = Column(String(350))
    publico_infantil: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    publicio_adulto: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))

