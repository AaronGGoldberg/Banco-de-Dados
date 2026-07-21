# Ramon-Couto_Aaron-Guerra

# TP1 - Sistema de Acompanhamento de Treinos de Corrida

## Descrição

Este projeto foi desenvolvido para a disciplina de Programação de Banco de Dados.
O objetivo é criar um banco de dados para um sistema de acompanhamento de treinos de corrida, permitindo gerenciar instrutores, alunos, grupos, planos, contratos, cronogramas e treinos.

## Tecnologias utilizadas

* PostgreSQL
* Python
* psycopg2
* python-dotenv
* tabulate

## Estrutura do projeto

sql/
├── schema.sql
├── seed.sql
└── queries/
  ├── Q01.sql até Q10.sql

config/
├── database.py

main.py
.env.example

## Como executar

### 1. Criar o banco de dados

No PostgreSQL, criar o banco:

CREATE DATABASE treinos_corrida;

### 2. Executar os scripts SQL

psql -d treinos_corrida -f sql/schema.sql
psql -d treinos_corrida -f sql/seed.sql

### 3. Configurar o arquivo .env

Criar um arquivo .env baseado no .env.example:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=treinos_corrida
DB_USER=postgres
DB_PASS=postgres

Obs: caso esteja usando porta ou usuário diferente, ajustar conforme o ambiente.

### 4. Instalar dependências

pip install psycopg2-binary python-dotenv tabulate

### 5. Executar a aplicação

python main.py

## Funcionalidades

O sistema possui uma interface de linha de comando (CLI) com um menu contendo 10 opções:

1. Listar alunos de um instrutor
2. Alunos e planos ativos
3. Treinos de um aluno no mês
4. Grupos e quantidade de alunos
5. Cronogramas da semana atual
6. Total de km por aluno no mês
7. Alunos sem contrato ativo
8. Alunos acima da meta do cronograma
9. Valor total pago por aluno
10. Instrutores e total de alunos

## Observações

* As consultas SQL estão separadas em arquivos individuais na pasta `sql/queries/`.
* A conexão com o banco é feita através de variáveis de ambiente.
* Os resultados das consultas são exibidos em formato de tabela no terminal.
* O projeto foi desenvolvido com foco em aprendizado e prática dos conceitos de banco de dados.
