from sqlalchemy import Column, Integer, String, Text
from core.configs import settings


class PerguntasModel(settings.DBBaseModelJEDi):
    __tablename__ = 'pergunta2'

    id = Column(Integer, primary_key=True)
    id_tema = Column(Integer)
    pergunta = Column(Text, nullable=False)
    respcerta = Column(Text, nullable=False)
    resp2 = Column(Text)
    resp3 = Column(Text)
    resp4 = Column(Text)
    caminhoimagem = Column(String(50))
    tempo_leitura_adulto = Column(Integer)
    tempo_leitura_infantil = Column(Integer)
    numero_palavras = Column(Integer)
    numero_caracteres = Column(Integer)
