import requests
import json
import os

url = 'https://guilhermeonrails.github.io/api-restaurantes/restaurantes.json'
response = requests.get(url)
print(response)
if response.status_code == 200:
    dados_json = response.json()
    # print(dados_json)
    dados_restaurantes = {}
    for item in dados_json:
        nome_do_restaurante = item['Company']
        if nome_do_restaurante not in dados_restaurantes:
            dados_restaurantes[nome_do_restaurante] = []

        dados_restaurantes[nome_do_restaurante].append({
            'item': item['Item'],
            'price': item['price'],
            'description': item['description']
        })

    # 1. Garante que a pasta existe
    pasta_destino = "arqs"
    os.makedirs(pasta_destino, exist_ok=True)

    for nome_do_restaurante, dados in dados_restaurantes.items():
        nome_do_arquivo = f'{nome_do_restaurante}.json'
        caminho_arquivo = os.path.join(pasta_destino, nome_do_arquivo)

        with open(caminho_arquivo, 'w+') as arquivo_restaurante:
            json.dump(dados, arquivo_restaurante, indent=4)
else:
    print('f O erro foi {response.status_code}')

# print(dados_restaurantes['McDonald’s'])
