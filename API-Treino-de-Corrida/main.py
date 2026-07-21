import os
from tabulate import tabulate
from config.database import conectar

def ler_sql(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()

def executar_consulta(arquivo_sql):
    conn = conectar()

    if conn is None:
        return

    try:
        cursor = conn.cursor()
        sql = ler_sql(arquivo_sql)
        cursor.execute(sql)

        resultados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]

        print()
        print(tabulate(resultados, headers=colunas, tablefmt="grid"))
        print()

        cursor.close()
        conn.close()

    except Exception as e:
        print("Erro ao executar a consulta.")
        print(e)

def mostrar_menu():
    print("===== MENU =====")
    print("1. Listar alunos de um instrutor")
    print("2. Alunos e planos ativos")
    print("3. Treinos de um aluno no mês")
    print("4. Grupos e quantidade de alunos")
    print("5. Cronogramas da semana atual")
    print("6. Total de km por aluno no mês")
    print("7. Alunos sem contrato ativo")
    print("8. Alunos acima da meta do cronograma")
    print("9. Valor total pago por aluno")
    print("10. Instrutores e total de alunos")
    print("0. Sair")
    print("q. Sair")

arquivos = {
    "1": "sql/queries/Q01.sql",
    "2": "sql/queries/Q02.sql",
    "3": "sql/queries/Q03.sql",
    "4": "sql/queries/Q04.sql",
    "5": "sql/queries/Q05.sql",
    "6": "sql/queries/Q06.sql",
    "7": "sql/queries/Q07.sql",
    "8": "sql/queries/Q08.sql",
    "9": "sql/queries/Q09.sql",
    "10": "sql/queries/Q10.sql"
}

while True:
    mostrar_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "0" or opcao.lower() == "q":
        print("Saindo...")
        break

    if opcao in arquivos:
        executar_consulta(arquivos[opcao])
    else:
        print("Opção inválida.")