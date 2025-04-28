# Essas são as bibliotecas utilizadas no projeto
from datetime import datetime, timezone, timedelta
import sqlite3
# configurações do estacionamento
capacidade = 10
dicprecos = {
    "precoate1h": 10,
    "precoate2h": 15,
    "precoate3h": 30,
    "precoate4h": 50,
    "precodiaria": 70
}
fuso = timezone(timedelta(hours=-3))
horariolocal = datetime.now(fuso)
def criarbanco():
    conexao = sqlite3.connect('estacionamento.db')
    cursor = conexao.cursor()
    # criação da tabela no banco de dados:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        tipo TEXT NOT NULL,
        entrada DATETIME,
        saida DATETIME               
    )
    ''')
    conexao.commit()
    conexao.close()

# Essa função deverá registrar o carro
def entrada():
    conexao = sqlite3.connect('estacionamento.db')
    cursor = conexao.cursor()    
    while True:
        placa = (str(input('Insira a placa do veículo: ').replace(" ","")).upper())
        if len(placa) == 7:
            break
        else:
            print('Placa inválida! Insira novamente.')

    if not verificar_estacionamento(placa):
        return
    if not status():
        return

    while True:
        try:
            tipo = int(input('''Insira o tipo do veículo:

    [1] Carro
    [2] Moto
    [3] Caminhão
----> '''))

            if tipo in [1, 2, 3]:
                tipo_nome = {1: 'Carro', 2: 'Moto', 3: 'Caminhão'}[tipo]
                break
            else:
                print('O tipo de veículo digitado não é válido. Insira 1, 2 ou 3.')
        except ValueError:
            print('Tipo de veículo inválido! Insira um número.')

    horario_entrada = datetime.now(fuso).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        'INSERT INTO veiculos (placa, tipo, entrada) VALUES (?, ?, ?)',
        (placa, tipo_nome, horario_entrada)
    )
    conexao.commit()
    conexao.close()
    hora_local = datetime.now(fuso).strftime("%H:%M")
    print(f"✅ Veículo registrado: {placa[:3]}-{placa[3:]} | Tipo: {tipo_nome}, Horário de entrada (UTC): {hora_local}")


def saida():
    placa = str(input('Insira a placa do veículo: ').replace(" ","").upper())
    conec = sqlite3.connect('estacionamento.db')
    cur = conec.cursor()
    cur.execute("SELECT * FROM veiculos WHERE placa = ? AND saida IS NULL", (placa,))
    reg = cur.fetchone()

    if reg:
        entrada_utc = datetime.strptime(reg[3], "%Y-%m-%d %H:%M:%S")  # Entrada no formato UTC
        entrada_local = entrada_utc.astimezone(fuso)  # Convertendo para horário local

        saida_utc = datetime.utcnow().replace(tzinfo=timezone.utc)  # Garantir que a saída também tem fuso horário UTC

        tempo_total = saida_utc - entrada_local  # Agora os dois têm o mesmo fuso horário
        permanencia = int(tempo_total.total_seconds() // 3600)

        if permanencia < 1:
            preco = dicprecos["precoate1h"]
        elif permanencia < 2:
            preco = dicprecos["precoate2h"]
        elif permanencia < 3:
            preco = dicprecos["precoate3h"]
        elif permanencia < 4:
            preco = dicprecos["precoate4h"]
        else:
            preco = dicprecos["precodiaria"]
        
        cur.execute(
            "UPDATE veiculos SET saida = ? WHERE placa = ? AND saida IS NULL",
            (saida_utc.strftime("%Y-%m-%d %H:%M:%S"), placa)
        )
        conec.commit()
        conec.close()
        print(f"✅ Saída registrada para o veículo {placa}")
        print(f"⏱ Tempo de permanência: {permanencia} hora(s)")
        print(f"💰 Valor a pagar: R$ {preco:.2f}")
    else:
        print('O veículo não foi encontrado no sistema do estacionamento')
        conec.close()

# Essa função vai ser responsável por gerar o relatório do estacionamento
def relatorio():
    conection = sqlite3.connect('estacionamento.db')
    cursor = conection.cursor()
    cursor.execute("SELECT * FROM veiculos WHERE saida IS NOT NULL")
    resposta = cursor.fetchall()

    if not resposta:
        print('Não houve movimentação!')
    else:
        def formatar_tabela(dados, cabecalho):
            larguras = [len(col) for col in cabecalho]
            for linha in dados:
                for i, item in enumerate(linha):
                    larguras[i] = max(larguras[i], len(str(item)))

            def formatar_linha(linha):
                return "  ".join(f"{str(item):<{larguras[i]}}" for i, item in enumerate(linha))

            print(formatar_linha(cabecalho))
            print("-" * (sum(larguras) + len(larguras) * 2))

            for linha in dados:
                print(formatar_linha(linha))

        formatar_tabela(resposta, ["ID", "Placa", "Tipo", "Entrada", "Saída"])

    conection.close()



# função responsável por verificar se o carro já está estacionado para permitir que seja dada a entrada no estacionamento
def verificar_estacionamento(placa):
    conection = sqlite3.connect('estacionamento.db')
    cursor = conection.cursor()
    cursor.execute("SELECT * FROM veiculos WHERE placa = ? AND saida IS NULL", (placa,))
    resultado = cursor.fetchone()
    conection.close()
    if resultado:
        print("O veículo já está estacionado!")
        return False  
    else:
        return True 

def status():
    conexao = sqlite3.connect('estacionamento.db')
    cursor = conexao.cursor() 
    cursor.execute("SELECT COUNT(*) FROM veiculos WHERE saida IS NULL")
    total_estacionados = cursor.fetchone()[0]
    conexao.close()
    if total_estacionados >= capacidade:
        print('🚫 Estacionamento lotado.')
        return False
    return True
