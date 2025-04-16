from estacionamento import *
import sqlite3
conexao = sqlite3.connect('PCDPI/estacionamento.db')
cursor = conexao.cursor()
def status():
    while True:
        cursor.execute('SELECT COUNT * FROM veiculos WHERE saida = 0')
        ocupacao = cursor.fetchone()[0]
        if ocupacao == limite:
            print('Estacionamento ocupado')

def menu():
    status()
