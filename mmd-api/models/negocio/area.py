from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.configs import settings


class AreaModel(settings.DBBaseModelJEDi):
    __tablename__ = 'area2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

    # Relacionamentos
    temas = relationship("TemaModel", back_populates="area")


