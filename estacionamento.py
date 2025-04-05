#primeiramente vamos considerar um estacionamento 20 com vagas sendo corredores A e B com 10 vagas cada.
vagas = []
for i in range (2):
    corredor = []
    for j in range(10):
        corredor.append(0)
    vagas.append(corredor)
for corredor in vagas:
    print(corredor)
#aqui vamos definir o que vai aparecer no painel da entrada do estacionamento.

if all(all(corredor == 1)):
    disponibilidade = ('Lotado')
else: disponibilidade = ('Há vagas')
print('Disponibilidade')

