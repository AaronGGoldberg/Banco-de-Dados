# API REST de Livraria

## Integrantes

* Aaron Guerra Goldberg - 20251014040042
* Fernando Yuri Vital de Aquino - 20231014040022

## Domínio Escolhido

Livraria

## Descrição

Este trabalho consiste no desenvolvimento de uma API REST utilizando Node.js, Express, PostgreSQL e Sequelize.

O sistema permite realizar operações de cadastro, consulta, atualização e remoção de livros armazenados no banco de dados PostgreSQL.

---

## Recurso Principal

Livro

Campos utilizados:

* id
* titulo
* autor
* editora
* isbn
* preco
* estoque
* ano_publicacao
* createdAt
* updatedAt

---

## Tecnologias Utilizadas

* Node.js
* Express
* PostgreSQL
* Sequelize
* Sequelize CLI
* Dotenv

---

## Instalação do Projeto

Primeiro foi necessário instalar as dependências:

```bash
npm install
```

Também foram instalados os pacotes utilizados pela API:

```bash
npm install express sequelize pg pg-hstore dotenv
npm install --save-dev sequelize-cli nodemon
```

---

## Configuração do PostgreSQL

Durante o desenvolvimento no GitHub Codespaces foi necessário instalar o PostgreSQL manualmente.

Instalação:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

Entrar no usuário postgres:

```bash
sudo su postgres
```

Abrir o PostgreSQL:

```bash
psql
```

Criar o banco:

```sql
CREATE DATABASE pabd_livraria;
```

Definir senha do usuário postgres:

```sql
ALTER USER postgres PASSWORD 'postgres';
```

Listar bancos:

```sql
\l
```

Sair:

```sql
\q
```

---

## Variáveis de Ambiente

Arquivo `.env` utilizado:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pabd_livraria
DB_USER=postgres
DB_PASSWORD=postgres
PORT=3000
```

---

## Executando as Migrations

Para criar a tabela no banco:

```bash
npx sequelize-cli db:migrate
```

Para verificar o status:

```bash
npx sequelize-cli db:migrate:status
```

---

## Executando a Aplicação

Para iniciar o servidor:

```bash
npm run dev
```

A API ficará disponível em:

```text
http://localhost:3000
```

---

# Endpoints

## Listar todos os livros

```http
GET /livros
```

Exemplo:

```bash
curl http://localhost:3000/livros
```

Resposta:

```json
[
  {
    "id": 1,
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "editora": "Principis",
    "isbn": "9788594318601",
    "preco": "29.90",
    "estoque": 10,
    "ano_publicacao": 1899
  }
]
```

---

## Buscar livro por ID

```http
GET /livros/:id
```

Exemplo:

```bash
curl http://localhost:3000/livros/1
```

Resposta:

```json
{
  "id": 1,
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "editora": "Principis",
  "isbn": "9788594318601",
  "preco": "29.90",
  "estoque": 10,
  "ano_publicacao": 1899
}
```

---

## Cadastrar livro

```http
POST /livros
```

Exemplo:

```bash
curl -X POST http://localhost:3000/livros \
-H "Content-Type: application/json" \
-d '{
  "titulo":"Dom Casmurro",
  "autor":"Machado de Assis",
  "editora":"Principis",
  "isbn":"9788594318601",
  "preco":29.90,
  "estoque":10,
  "ano_publicacao":1899
}'
```

---

## Atualizar livro

```http
PUT /livros/:id
```

Exemplo:

```bash
curl -X PUT http://localhost:3000/livros/1 \
-H "Content-Type: application/json" \
-d '{
  "titulo":"Dom Casmurro",
  "autor":"Machado de Assis",
  "editora":"Principis",
  "isbn":"9788594318601",
  "preco":35.90,
  "estoque":8,
  "ano_publicacao":1899
}'
```

---

## Remover livro

```http
DELETE /livros/:id
```

Exemplo:

```bash
curl -X DELETE http://localhost:3000/livros/1
```

---

