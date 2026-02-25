from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get('/api/hello')
def hello_world():
    '''
    Endpoint que exibe uma mensagem incrível do mundo da programação.
    '''
    return {'Hello':'World'}

@app.get('/api/restaurantes/')
def get_restaurantes(restaurante: str = Query(None)):
    '''
    Endpoint para ver o cardápio dos restaurantes.
    
    :param restaurante: Description
    :type restaurante: str
    '''

    url = 'https://guilhermeonrails.github.io/api-restaurantes/restaurantes.json'
    response = requests.get(url)

    if response.status_code == 200:
        dados_json = response.json()
        if restaurante is None:
            return {
                'dados': dados_json
            }

        dados_restaurantes = []
        for item in dados_json:
            if item['Company'] == restaurante:
                dados_restaurantes.append({
                    'item': item['Item'],
                    'price': item['price'],
                    'description': item['description']
                })

        return {
            'Restaurante': restaurante,
            'Cardapio': dados_restaurantes
        }
    else:
        return {
            'Erro': f'{response.status_code} - {response.text}'
        }
