import manterAluno
acad = "on"


while (acad != "off"):
    print("""
    -------------| Bem Vindo! |-------------
    | 1 - Cadastrar Aluno               
    | 2 - Lista de Alunos          
    | 3 - Gerenciar Aluno          
    | 4 -          
    | 5 -       
    | 6 - Finalizar Programa           
    ------------------------------------
    """) 
    painel = int(input("Selecione um número: "))
    match painel:
        case 1:
            manterAluno.cadAluno()
        case 2:
            manterAluno.listarAlunos()
        case 3:
            manterAluno.gerenciarAluno()
        case 6:
            acad = "off"
        case _:
            print("Opção inválida!!")