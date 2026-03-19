import spacy
from wordcloud import WordCloud
from api.v1.endpoints.utils.utils import gerar_nuvem_palavras

class NuvemPalavarasService:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    async def processar_texto_e_gerar_nuvem(self, registros, path_relativo):
        # Unificando o texto
        texto_completo = " ".join([reg.pergunta for reg in registros])
        
        # Processamento spaCy (Lematização)
        doc = self.nlp(texto_completo.lower())
        palavras_limpas = [
            token.lemma_ for token in doc 
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        
        texto_final = " ".join(palavras_limpas)

        # Configuração da Nuvem
        nuvem = WordCloud(
            width=800, height=400, background_color='white',
            colormap='viridis', max_words=100
        ).generate(texto_final)

        await gerar_nuvem_palavras(nuvem, path_relativo)
        
        return texto_completo