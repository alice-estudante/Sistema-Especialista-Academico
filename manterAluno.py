import csv

def salvar(alunos):
    
    with open("alunos.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerows(alunos)

def cadAluno():
    cpf = int(input("CPF: "))
    nome = input("Nome: ")
    dataNasc = input("Data de Nascimento: ")
    mat = int(input("Matricula: "))
    nota1 = float(input("Nota 1: "))
    nota2 = float(input("Nota 2: "))

    with open("alunos.csv", "a", newline="", encoding="utf-8") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow([cpf, nome, dataNasc, mat, nota1, nota2])

def listarAlunos():
    with open("alunos.csv", "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        for linha in leitor:
            print(linha) 

def gerenciarAluno():
    cpf = int(input("Digite o CPF do aluno que deseja gerenciar: "))
    with open("alunos.csv", "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        alunos = list(leitor)

    for i, aluno in enumerate(alunos):
        if int(aluno[0]) == cpf:
            print(f"Aluno encontrado: {aluno}")
            print("""
            -------------| Gerenciar Aluno |-------------
            | 1 - Atualizar Dados               
            | 2 - Excluir Aluno          
            | 3 - Voltar          
            ------------------------------------
            """)
            opcao = int(input("Selecione uma opção: "))
            match opcao:
                case 1:
                    atualizarAluno(i, alunos)
                case 2:
                    excluirAluno(i, alunos)
                case 3:
                    return
                case _:
                    print("Opção inválida!!")
            break
    else:
        print("Aluno não encontrado.")


def excluirAluno(indice, alunos):
    # Exibe o nome do aluno que será removido para confirmação
    removido = alunos[indice]
    print(f"\nTem certeza que deseja excluir o aluno: {removido[1]}?")
    confirmacao = input("Digite 'S' para confirmar ou qualquer tecla para cancelar: ").upper()

    if confirmacao == "S" or confirmacao == "SIM" or confirmacao == "s" or confirmacao == "sim":
        alunos.pop(indice)
        
        salvar(alunos)
        print("\nAluno excluído com sucesso!")
    else:
        print("\nOperação cancelada.")

def atualizarAluno(indice, alunos):
    print("\n--- Atualizar Dados do Aluno (pressione Enter para manter o valor atual) ---")
    aluno = alunos[indice]

    nome = input(f"Novo Nome [{aluno[1]}]: ") or aluno[1]
    dataNasc = input(f"Nova Data de Nasc. [{aluno[2]}]: ") or aluno[2]
    
    mat_in = input(f"Nova Matrícula [{aluno[3]}]: ")
    mat = int(mat_in) if mat_in else aluno[3]

    n1_in = input(f"Nova Nota 1 [{aluno[4]}]: ")
    nota1 = float(n1_in) if n1_in else aluno[4]

    n2_in = input(f"Nova Nota 2 [{aluno[5]}]: ")
    nota2 = float(n2_in) if n2_in else aluno[5]

    alunos[indice] = [aluno[0], nome, dataNasc, mat, nota1, nota2]

    salvar(alunos)

    print("\nDados atualizados com sucesso!")

