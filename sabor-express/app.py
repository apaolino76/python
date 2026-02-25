import os

restaurantes = [
    {'nome': 'Praça', 'categoria': 'Japonesa', 'ativo': False},
    {'nome': 'Pizza Suprema', 'categoria': 'Italiana', 'ativo': True},
    {'nome': 'Cantina', 'categoria': 'Italiana', 'ativo': False}
]

def exibir_nome_do_programa():
    print("""
      
░██████╗░█████╗░██████╗░░█████╗░██████╗░  ███████╗██╗░░██╗██████╗░██████╗░███████╗░██████╗░██████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝
╚█████╗░███████║██████╦╝██║░░██║██████╔╝  █████╗░░░╚███╔╝░██████╔╝██████╔╝█████╗░░╚█████╗░╚█████╗░
░╚═══██╗██╔══██║██╔══██╗██║░░██║██╔══██╗  ██╔══╝░░░██╔██╗░██╔═══╝░██╔══██╗██╔══╝░░░╚═══██╗░╚═══██╗
██████╔╝██║░░██║██████╦╝╚█████╔╝██║░░██║  ███████╗██╔╝╚██╗██║░░░░░██║░░██║███████╗██████╔╝██████╔╝
╚═════╝░╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝  ╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░
      """)

def exibir_opcoes():
    print('1. Cadastrar Restaurante')
    print('2. Listar Restaurante')
    print('3. Ativar Restaurante')
    print('4. Sair\n')

def finalizar_app():
    exibir_subtitulo('Finalizando o app')

def voltar_ao_menu_principal():
    input('\nDigite uma tecla para voltar ao menu principal ')
    main()

def opcao_invalida():
    print('Opção Inválida!\n')
    voltar_ao_menu_principal()

def exibir_subtitulo(subtitulo):
    os.system('cls')
    linha = '*' * len(subtitulo)
    print(linha)
    print(subtitulo)
    print(linha)
    print()

def cadastrar_restaurante():
    exibir_subtitulo('Cadastro de Novos Restaurantes')
    nome = input('Nome: ')
    categoria = input('Categoria: ')
    dados = {'nome': nome, 'categoria': categoria, 'ativo': False}
    restaurantes.append(dados)
    print(f'O restaurante {nome} foi cadastrado com sucesso!\n')
    voltar_ao_menu_principal()

def listar_restaurantes():
    exibir_subtitulo('Listar restaurantes')
    
    print(f'{'Nome'.ljust(22)} | {'Categoria'.ljust(20)} | {'Status'}')
    for restaurante in restaurantes:
        nome = restaurante['nome']
        categoria = restaurante['categoria']
        ativo = 'ativado' if restaurante['ativo'] else 'desativado'
        print(f'- {nome.ljust(20)} | {categoria.ljust(20)} | {ativo}')
    
    voltar_ao_menu_principal()

def alternar_status_restaurante():
    exibir_subtitulo('Alterando o status do restaurante')
    nome = input('Digite o nome do restaurante : ')
    restaurante_encontrado = False
    for restaurante in restaurantes:
        if nome == restaurante['nome']:
            restaurante_encontrado = True
            restaurante['ativo'] = not restaurante['ativo']
            mensagem = f'O restaurante {nome} foi restaurado com sucesso' if restaurante['ativo'] else f'O restaurante {nome} foi desativado com sucesso'
            print(mensagem)
    
    if not restaurante_encontrado:
        print('O restaurante não foi encontrado')

    voltar_ao_menu_principal()


def escolher_opcao():
    # opcao_escolhida = int(input('Escolha uma opção: '))
    # print(opcao_escolhida == 1)
    # print(type(opcao_escolhida))
    # print(type(1))
    # opcao_escolhida = int(opcao_escolhida)
    # print(f'Você escolheu a opção {opcao_escolhida}')

    # if opcao_escolhida == 1:
    #    print('Cadastrar Restaurante')
    # elif opcao_escolhida == 2:
    #    print('Listar Restaurante')
    # elif opcao_escolhida == 3:
    #    print('Ativar Restaurante')
    # else:
    #    finalizar_app()

    try:
        opcao_escolhida = int(input('Escolha uma opção: '))
        if opcao_escolhida == 1:
            cadastrar_restaurante()
        elif opcao_escolhida == 2:
            listar_restaurantes()
        elif opcao_escolhida == 3:
            alternar_status_restaurante()
        elif opcao_escolhida == 4:
            finalizar_app()
        else:
            opcao_invalida()

        # match opcao_escolhida:
        #     case 1:
        #         # print('Adicionar restaurante')
        #         cadastrar_restaurante()
        #     case 2:
        #         listar_restaurantes()
        #     case 3:
        #         print('Ativar restaurante')
        #     case 4:
        #         finalizar_app()
        #     case _:
        #         opcao_invalida()
    except:
        opcao_invalida()

def main():
    os.system('cls')
    exibir_nome_do_programa()
    exibir_opcoes()
    escolher_opcao()

if __name__ == '__main__':
    main()

