import sqlite3

conexao = sqlite3.connect('estacionamento.db')
cursor = conexao.cursor()

# Apaga a tabela
cursor.execute("DROP TABLE IF EXISTS veiculos")

# Recria a tabela com a coluna 'saida'
cursor.execute('''
CREATE TABLE veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL,
    tipo TEXT NOT NULL,
    entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
    saida DATETIME               
)
''')

conexao.commit()
conexao.close()

print("✅ Tabela 'veiculos' foi resetada com sucesso.")
