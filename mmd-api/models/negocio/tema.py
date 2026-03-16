from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class TemaModel(settings.DBBaseModelJEDi):
    __tablename__ = 'tema2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    id_area = Column(Integer, ForeignKey("area2.id"))
    visibilidade = Column(String(20))
    idautor = Column(Integer)

    # Relacionamentos
    area = relationship("AreaModel", back_populates="temas")
    perguntas = relationship("PerguntasModel", back_populates="tema")
