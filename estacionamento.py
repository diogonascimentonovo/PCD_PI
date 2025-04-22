#import do arquivo que definimos as funções utilizadas no menu
from defs import *
#Esse é o menu interativo do usuário que é integrado às funções definidas no outro arquivo
criarbanco()
while True:
    try: 
        opcao = int(input('''
Escolha uma opção:
    [1] Entrada de veículo
    [2] Saída de veículo
    [3] Gerar relatório                                                   
---> '''))

        funcoes = {
            1: entrada,     
            2: saida,
            3: relatorio
        }

        if opcao in funcoes:
            funcoes[opcao]()
        else:
            print('Opção inválida, escolha 1, 2 ou 3.')

    except ValueError: 
        print('Opção inválida, insira um número inteiro!')
