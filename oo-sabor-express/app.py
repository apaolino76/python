from modelos.restaurante import Restaurante
from modelos.cardapio.bebida import Bebida
from modelos.cardapio.prato import Prato

restaurante_praca = Restaurante('praça', 'Gourmet')

bebida_suco = Bebida('Suco de Melancia', 5.0, 'grande')
bebida_suco.aplicar_desconto()

prato_paozinho = Prato('Pãozinho', 2.0, 'O melhor pão da cidade')
prato_paozinho.aplicar_desconto()

restaurante_praca.adicionar_no_cardapio(bebida_suco)
restaurante_praca.adicionar_no_cardapio(prato_paozinho)

# restaurante_praca.receber_avaliacao('Gui', 10)
# restaurante_praca.receber_avaliacao('Lais', 8)
# restaurante_praca.receber_avaliacao('Emy', 5)

# restaurante_mexicano = Restaurante('mexican food', 'Mexicana')
# restaurante_mexicano.alternar_estado()
# restaurante_japones = Restaurante('Japa', 'Japonesa')

def main():
    # Restaurante.listar_restaurantes()
    # print(bebida_suco)
    # print(prato_paozinho)
    restaurante_praca.exibir_cardapio

if __name__ == '__main__':
    main()