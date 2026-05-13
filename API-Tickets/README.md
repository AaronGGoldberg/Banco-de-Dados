# README.md — Sistema de Bilhetagem de Transporte Público

# Sistema de Bilhetagem de Transporte Público

Projeto desenvolvido utilizando Django REST Framework com PostgreSQL.

O objetivo do sistema é simular uma plataforma de transporte público contendo:

* gerenciamento de usuários
* empresas de transporte
* municípios
* tickets/passagens
* validações
* integração tarifária
* relatórios analíticos
* dashboard empresarial

---

# Tecnologias Utilizadas

## Backend

* Python
* Django
* Django REST Framework

## Banco de Dados

* PostgreSQL

## Documentação

* Swagger
* ReDoc

## Filtros

* django-filter

---

# Estrutura Geral do Projeto

O projeto foi organizado da seguinte forma:

```text
API-Tickets/
│
├── bilhetagem/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│
├── transporte_api/
│   ├── settings.py
│   ├── urls.py
│
├── api_transporte.http
├── manage.py
├── README.md
├── README_PROVA.md
```

---

# Criação do Projeto do Zero

# PASSO 1 — Criar pasta do projeto

```bash
mkdir API-Tickets
cd API-Tickets
```

## Explicação

mkdir cria uma pasta.

cd entra na pasta.

---

# PASSO 2 — Criar ambiente virtual

```bash
python -m venv venv
```

## Explicação

O ambiente virtual serve para isolar as bibliotecas Python do projeto.

Sem isso:

* bibliotecas poderiam conflitar
* versões poderiam quebrar outros projetos

---

# PASSO 3 — Ativar ambiente virtual

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

## Como saber se funcionou?

O terminal passa a mostrar:

```text
(venv)
```

no início da linha.

---

# PASSO 4 — Instalar Django

```bash
pip install django
```

---

# PASSO 5 — Criar projeto Django

```bash
django-admin startproject transporte_api .
```

## Explicação

transporte_api = nome do projeto

O ponto final significa:

"criar na pasta atual"

---

# PASSO 6 — Criar App

```bash
python manage.py startapp bilhetagem
```

---

# PASSO 7 — Instalar bibliotecas necessárias

```bash
pip install djangorestframework
pip install psycopg2-binary
pip install django-filter
pip install drf-yasg
```

---

# Configuração do PostgreSQL

# PASSO 1 — Iniciar PostgreSQL

```bash
sudo service postgresql start
```

## Explicação

sudo = executa como administrador

service = gerencia serviços Linux

postgresql = serviço do banco

start = iniciar

---

# PASSO 2 — Entrar no usuário postgres

```bash
sudo su postgres
```

## Explicação

sudo = permissões administrativas

su = switch user

postgres = usuário do PostgreSQL

---

# PASSO 3 — Entrar no terminal PostgreSQL

```bash
psql
```

---

# PASSO 4 — Criar banco

```sql
CREATE DATABASE transporte_db;
```

---

# PASSO 5 — Alterar senha do postgres

```sql
ALTER USER postgres PASSWORD '123';
```

---

# PASSO 6 — Dar permissões

```sql
GRANT ALL PRIVILEGES ON DATABASE transporte_db TO postgres;
```

---

# Problema Real Encontrado — permission denied for schema public

Erro encontrado:

```text
permission denied for schema public
```

## O que significa?

O usuário postgres não possuía permissão suficiente sobre o schema public.

## O que é schema?

Schema é uma organização interna do PostgreSQL.

O schema public é onde normalmente ficam as tabelas.

---

# Solução do Problema

Entrar no PostgreSQL:

```bash
sudo su postgres
psql
```

Executar:

```sql
GRANT ALL ON SCHEMA public TO postgres;
```

Depois disso:

```bash
python manage.py migrate
```

funcionou corretamente.

---

# Configuração do settings.py

Arquivo:

```text
transporte_api/settings.py
```

---

# INSTALLED_APPS

Adicionar:

```python
'rest_framework',
'django_filters',
'drf_yasg',
'bilhetagem',
```

---

# Configuração DATABASES

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'transporte_db',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

# Problema Real — Origin checking failed

Erro:

```text
Origin checking failed
```

## Motivo

O Codespaces usa domínio externo.

O Django bloqueia por segurança.

---

# Solução

Adicionar em settings.py:

```python
CSRF_TRUSTED_ORIGINS = [
    'https://*.app.github.dev',
    'https://*.githubpreview.dev',
]
```

---

# Problema Real — API Root usando localhost

Problema:

O Django REST Framework gerava URLs usando localhost.

No Codespaces isso quebrava.

---

# Solução

Adicionar:

```python
USE_X_FORWARDED_HOST = True
```

Também:

```python
SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https'
)
```

---

# Migrations

# Criar migrations

```bash
python manage.py makemigrations
```

# Aplicar migrations

```bash
python manage.py migrate
```

---

# Models do Sistema

O sistema possui:

* Municipio
* EmpresaTransporte
* Usuario
* TipoTicket
* Ticket
* Transporte
* Validador
* Validacao

---

# Explicação dos Relacionamentos

## ForeignKey

Usado para relacionar tabelas.

Exemplo:

```python
empresa = models.ForeignKey(EmpresaTransporte)
```

Isso significa:

Um transporte pertence a uma empresa.

---

# Serializers

Arquivo:

```text
serializers.py
```

## Função

Transformar objetos Python em JSON.

E validar dados recebidos.

---

# ViewSets

Arquivo:

```text
views.py
```

## Função

Controlar:

* GET
* POST
* PUT
* PATCH
* DELETE

---

# Router

Arquivo:

```text
urls.py
```

Usamos:

```python
DefaultRouter
```

para gerar automaticamente as rotas.

---

# Swagger

Endpoints:

```text
/swagger/
/redoc/
```

---

# Funcionalidades Implementadas

# CRUD Completo

Sistema possui CRUD completo para:

* municípios
* empresas
* usuários
* tickets
* validadores
* transportes

---

# Recarga de Saldo

Endpoint:

```text
/usuarios/{id}/recarregar/
```

Permite adicionar saldo ao usuário.

---

# Integração Tarifária

O sistema verifica:

* se existe validação anterior
* se está dentro da janela de integração

Se estiver:

* não cobra nova tarifa

---

# Extrato

Endpoint:

```text
/usuarios/{id}/extrato/
```

Retorna:

* saldo
* tickets ativos
* tickets expirados
* validações
* economia integração

---

# Relatório Transporte

Endpoint:

```text
/transportes/{id}/relatorio/
```

Retorna:

* receita
* validações
* usuários únicos
* distribuição tickets

---

# Painel Empresa

Endpoint:

```text
/empresas/{id}/painel/
```

Retorna:

* top 5 transportes
* métricas últimos 30 dias
* transportes ativos
* validadores ativos

---

# Relatório Município

Endpoint:

```text
/municipios/{id}/relatorio-geral/
```

Retorna:

* empresas concedidas
* receita total
* validações
* tickets vendidos

---

# Filtros

Usamos:

```python
filter_backends
```

---

# Busca

Usamos:

```python
search_fields
```

---

# Ordenação

Usamos:

```python
ordering_fields
```

---

# Funções SQL Avançadas

# Count

Conta registros.

---

# Sum

Soma valores.

---

# annotate

Cria campos calculados.

---

# aggregate

Faz agregações gerais.

---

# TruncDate

Agrupa por dia.

---

# Arquivo api_transporte.http

Arquivo criado para testar endpoints rapidamente.

Utilizado junto da extensão REST Client.

---

# Executar Servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

---

# Comandos Importantes

# Criar superusuário

```bash
python manage.py createsuperuser
```

---

# Verificar erros

```bash
python manage.py check
```

---

# Salvar dependências

```bash
pip freeze > requirements.txt
```

---

# Fluxo Geral do Sistema

```text
Usuário → saldo → compra ticket → validação → integração → relatórios
```

---

# Conclusão

O projeto implementa uma API REST completa de bilhetagem de transporte público.

Durante o desenvolvimento foram trabalhados:

* Django
* PostgreSQL
* REST APIs
* Swagger
* ReDoc
* relatórios analíticos
* integração tarifária
* regras de negócio
* problemas reais de ambiente no Codespaces
