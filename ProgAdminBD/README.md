# ProgAdminBD — Guia de Estudos (linguagem de estudante)

E aí! 👋

Este projeto foi organizado para acompanhar as aulas de **Programação e Administração de Banco de Dados** com **Django REST Framework (DRF)**.
A ideia aqui é deixar tudo simples: o que é cada arquivo, como rodar e como testar os endpoints sem complicação.

---

## 📚 Materiais adicionados nesta pasta

Foram adicionados os 3 guias pedidos:

1. **Introdução ao Django Rest Framework**  
   Arquivo: `Introducão-Django_REST_Framework.md`
2. **Continuação de Modelagem com Django Rest Framework**  
   Arquivo: `ContinuacãoModelagem-Django_REST_Framework.md`
3. **Relacionamento entre Modelos**  
   Arquivo: `Continuação-Relacionamento_Entre_Modelos.md`

Esses materiais seguem o passo a passo da aula, com foco prático.

---

## 🧱 O que tem na API hoje

Aplicação: `amazon`  
App principal: `backend`

### Modelos
- `Cliente`
- `Vendedor`
- `Produto`

### Endpoints principais
- `/amazon_api/clientes/`
- `/amazon_api/vendedores/`
- `/amazon_api/produtos/`

### Documentação automática
- Swagger UI: `/swagger/`
- Redoc: `/redoc/`
- JSON do schema: `/swagger.json`

---

## 🚀 Como rodar (passo a passo)

> Requisito: Python 3.10+ e PostgreSQL instalado.

1. Entrar na pasta do projeto Django:

```bash
cd ProgAdminBD/amazon
```

2. Criar e ativar ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instalar dependências:

```bash
pip install django djangorestframework django-filter drf-yasg django-cors-headers djangorestframework-simplejwt psycopg2-binary
```

4. Aplicar migrações:

```bash
python manage.py migrate
```

5. Subir servidor:

```bash
python manage.py runserver
```

6. Abrir no navegador:
- `http://127.0.0.1:8000/swagger/`

---

## 🧪 Como testar rápido

### Exemplo: criar vendedor (POST)
Endpoint: `/amazon_api/vendedores/`

JSON:

```json
{
  "nome": "Carlos Santos",
  "email": "carlos@email.com",
  "cpf": "123.456.789-00",
  "telefone": "(84) 99999-9999",
  "salario": "3500.00",
  "ativo": true
}
```

### Exemplo: listar produtos com filtro
- `/amazon_api/produtos/?categoria=eletronicos`
- `/amazon_api/produtos/?ordering=-preco`
- `/amazon_api/produtos/?search=notebook`

---

## 🎯 Objetivo pedagógico

Esse repositório agora está pronto para treinar:
- CRUD com DRF
- serializers
- viewsets + rotas automáticas
- filtros, busca e ordenação
- modelagem de tabelas no Django ORM
- evolução para relacionamentos entre modelos
