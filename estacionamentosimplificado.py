

# Capacidade total
TOTAL_VAGAS = 100

# Dicionário de vagas: chave = número da vaga, valor = dados do carro
vagas = {}

# Função para encontrar a próxima vaga disponível
def proxima_vaga_disponivel():
    for i in range(1, TOTAL_VAGAS + 1):
        if i not in vagas:
            return i
    return None

# Função para registrar a entrada
def registrar_entrada():
    if len(vagas) >= TOTAL_VAGAS:
        print("Estacionamento cheio.")
        return

    modelo = input("Modelo do carro: ")
    cor = input("Cor do carro: ")
    placa = input("Placa do carro: ").upper()
    hora_entrada = datetime.now()

    vaga = proxima_vaga_disponivel()

    vagas[vaga] = {
        "modelo": modelo,
        "cor": cor,
        "placa": placa,
        "entrada": hora_entrada,
        "saida": None
    }

    print(f"Carro estacionado na vaga {vaga} às {hora_entrada.strftime('%H:%M:%S')}.")

# Função para registrar a saída
def registrar_saida():
    placa = input("Informe a placa do veículo que vai sair: ").upper()

    for vaga, dados in list(vagas.items()):
        if dados["placa"] == placa:
            hora_saida = datetime.now()
            dados["saida"] = hora_saida
            tempo = hora_saida - dados["entrada"]
            del vagas[vaga]  # Libera a vaga
            print(f"Carro removido da vaga {vaga}.")
            print(f"Tempo de permanência: {str(tempo).split('.')[0]}")
            return

    print("Veículo não encontrado.")

# Função para mostrar status das vagas
def status_estacionamento():
    print(f"\nVagas ocupadas: {len(vagas)} / {TOTAL_VAGAS}")
    for vaga, dados in vagas.items():
        entrada = dados["entrada"].strftime('%H:%M:%S')
        print(f"Vaga {vaga}: {dados['modelo']} | {dados['cor']} | {dados['placa']} | Entrada: {entrada}")
    print("")

# Menu principal
def menu():
    while True:
        print("\n--- MENU ESTACIONAMENTO ---")
        print("1 - Registrar entrada")
        print("2 - Registrar saída")
        print("3 - Status do estacionamento")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            registrar_entrada()
        elif opcao == '2':
            registrar_saida()
        elif opcao == '3':
            status_estacionamento()
        elif opcao == '4':
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida!")

# Iniciar o programa
if __name__ == "__main__":
    menu()
