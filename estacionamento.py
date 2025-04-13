from defs import *
import sqlite3
conexao = sqlite3.connect('PCDPI/estacionamento.db')
cursor = conexao.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS veiculos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT,
    entrada TEXT,
    categoria INTEGER, 
    saida INTEGER DEFAULT 0
               )''')
conexao.commit()
conexao.close()
limite = 20
while True:
    cursor.execute('SELECT COUNT * FROM veiculos WHERE saida = 0')
    ocupacao = cursor.fetchone()[0]
    if ocupacao == limite:
        print('Estacionament ocupado')
