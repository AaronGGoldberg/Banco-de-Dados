# README_PROVA.md

# GUIA DEFINITIVO PARA PROVAS — DJANGO REST FRAMEWORK + POSTGRESQL

Este arquivo serve como um guia EXTREMAMENTE detalhado para recriar rapidamente um projeto parecido durante provas práticas.

Objetivo:

- criar APIs REST rapidamente
- configurar PostgreSQL
- resolver erros comuns
- usar Swagger
- criar CRUD
- fazer filtros
- criar relatórios
- sobreviver no Codespaces

Mesmo que você esqueça quase tudo.

---

# SUMÁRIO

1. Criar Projeto
2. Ambiente Virtual
3. Instalar Bibliotecas
4. PostgreSQL
5. Configurar Django
6. Resolver Problemas do Codespaces
7. Criar Models
8. Migrations
9. Serializers
10. Views/ViewSets
11. URLs
12. Swagger/ReDoc
13. Filtros
14. Endpoints Personalizados
15. Relatórios
16. Arquivo HTTP
17. Comandos Importantes
18. Erros Mais Comuns
19. Checklist Final

---

# 1 — CRIAR PASTA DO PROJETO

```bash
mkdir nome-projeto
cd nome-projeto
```

## Explicação

### mkdir
Cria uma pasta.

### cd
Entra na pasta criada.

---

# 2 — CRIAR AMBIENTE VIRTUAL

```bash
python -m venv venv
```

## Explicação

O ambiente virtual serve para:

- isolar bibliotecas
- evitar conflitos
- deixar o projeto independente

---

# 3 — ATIVAR AMBIENTE VIRTUAL

## Linux/macOS

```bash
source venv/bin/activate
```

## Windows

```bash
venv\Scripts\activate
```

---

# COMO SABER SE FUNCIONOU?

O terminal ficará assim:

```text
(venv)
```

no início da linha.

---

# 4 — INSTALAR DJANGO

```bash
pip install django
```

---

# 5 — CRIAR PROJETO DJANGO

```bash
django-admin startproject nome_projeto .
```

## Explicação

### nome_projeto
Nome principal do projeto.

### ponto final (.)
Significa:

"criar na pasta atual"

Sem o ponto:
o Django criaria outra pasta dentro da pasta atual.

---

# 6 — CRIAR APP

```bash
python manage.py startapp nome_app
```

## Explicação

O projeto Django é dividido em apps.

Exemplos:

- usuários
- vendas
- transporte
- estoque

---

# 7 — INSTALAR BIBLIOTECAS IMPORTANTES

```bash
pip install djangorestframework
pip install psycopg2-binary
pip install django-filter
pip install drf-yasg
```

---

# O QUE CADA BIBLIOTECA FAZ?

## djangorestframework

Cria APIs REST.

---

## psycopg2-binary

Conecta Django com PostgreSQL.

---

## django-filter

Permite filtros nos endpoints.

---

## drf-yasg

Cria Swagger e ReDoc automaticamente.

---

# 8 — CONFIGURAR INSTALLED_APPS

Arquivo:

```text
settings.py
```

Adicionar:

```python
INSTALLED_APPS = [
    ...

    'rest_framework',
    'django_filters',
    'drf_yasg',

    'nome_app',
]
```

---

# 9 — INICIAR POSTGRESQL

## No Codespaces/Linux

```bash
sudo service postgresql start
```

---

# O QUE ISSO FAZ?

## sudo
Executa como administrador.

---

## service
Gerencia serviços Linux.

---

## postgresql
Nome do serviço do banco.

---

## start
Inicia o serviço.

---

# 10 — ENTRAR NO USUÁRIO POSTGRES

```bash
sudo su postgres
```

---

# EXPLICAÇÃO

## sudo
Permissão administrativa.

---

## su
Switch User.

Troca de usuário.

---

## postgres
Usuário interno do PostgreSQL.

---

# 11 — ENTRAR NO TERMINAL POSTGRESQL

```bash
psql
```

---

# O QUE É O PSQL?

É o terminal SQL do PostgreSQL.

Nele podemos:

- criar bancos
- criar usuários
- alterar permissões
- executar SQL

---

# 12 — CRIAR BANCO

```sql
CREATE DATABASE banco_db;
```

---

# 13 — ALTERAR SENHA POSTGRES

```sql
ALTER USER postgres PASSWORD '123';
```

---

# 14 — DAR PERMISSÕES AO BANCO

```sql
GRANT ALL PRIVILEGES ON DATABASE banco_db TO postgres;
```

---

# 15 — PROBLEMA MUITO COMUM

# ERRO:

```text
permission denied for schema public
```

---

# O QUE SIGNIFICA?

O usuário postgres não possui permissão suficiente no schema public.

---

# O QUE É SCHEMA?

Schema é como uma organização interna do banco.

O schema public normalmente guarda as tabelas.

---

# SOLUÇÃO

Executar:

```sql
GRANT ALL ON SCHEMA public TO postgres;
```

---

# SAIR DO POSTGRESQL

```sql
\q
```

---

# VOLTAR AO TERMINAL NORMAL

```bash
exit
```

---

# 16 — CONFIGURAR DATABASES NO DJANGO

Arquivo:

```text
settings.py
```

Adicionar:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'banco_db',

        'USER': 'postgres',

        'PASSWORD': '123',

        'HOST': 'localhost',

        'PORT': '5432',
    }
}
```

---

# EXPLICAÇÃO

## ENGINE
Tipo do banco.

---

## NAME
Nome do banco.

---

## USER
Usuário PostgreSQL.

---

## PASSWORD
Senha PostgreSQL.

---

## HOST
Servidor do banco.

localhost = mesma máquina.

---

## PORT
Porta do PostgreSQL.

Padrão = 5432.

---

# 17 — CONFIGURAÇÕES IMPORTANTES CODESPACES

Adicionar no settings.py:

```python
ALLOWED_HOSTS = ['*']
```

---

# O QUE ISSO FAZ?

Permite acesso externo.

Sem isso:
o Django bloqueia.

---

# 18 — ERRO MUITO COMUM

# ERRO:

```text
Origin checking failed
```

---

# MOTIVO

O Codespaces usa domínio externo.

O Django bloqueia por segurança CSRF.

---

# SOLUÇÃO

Adicionar:

```python
CSRF_TRUSTED_ORIGINS = [
    'https://*.app.github.dev',
    'https://*.githubpreview.dev',
]
```

---

# 19 — ERRO MUITO COMUM

# PROBLEMA:

API Root usando localhost.

---

# MOTIVO

O Django REST Framework gera URLs absolutas.

No Codespaces:
localhost quebra.

---

# SOLUÇÃO

Adicionar:

```python
USE_X_FORWARDED_HOST = True
```

E também:

```python
SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https'
)
```

---

# 20 — CRIAR MODELS

Arquivo:

```text
models.py
```

---

# COMO PENSAR NOS MODELS?

Pergunta:

"Quais entidades existem?"

Exemplo:

- Usuario
- Produto
- Ticket
- Transporte
- Empresa

---

# TIPOS IMPORTANTES

# CharField

Texto curto.

```python
nome = models.CharField(max_length=100)
```

---

# TextField

Texto longo.

```python
descricao = models.TextField()
```

---

# IntegerField

Número inteiro.

```python
idade = models.IntegerField()
```

---

# DecimalField

Valores monetários.

```python
saldo = models.DecimalField(
    max_digits=10,
    decimal_places=2
)
```

---

# BooleanField

True ou False.

```python
ativo = models.BooleanField(default=True)
```

---

# DateTimeField

Datas.

```python
criado_em = models.DateTimeField(auto_now_add=True)
```

---

# ForeignKey

Relacionamento entre tabelas.

```python
empresa = models.ForeignKey(
    Empresa,
    on_delete=models.CASCADE
)
```

---

# O QUE É CASCADE?

Se a empresa for apagada:
os registros relacionados também serão.

---

# 21 — MIGRATIONS

# Criar migrations

```bash
python manage.py makemigrations
```

---

# Aplicar migrations

```bash
python manage.py migrate
```

---

# O QUE AS MIGRATIONS FAZEM?

Transformam os models em tabelas reais no banco.

---

# 22 — CRIAR SUPERUSUÁRIO

```bash
python manage.py createsuperuser
```

---

# 23 — RODAR SERVIDOR

```bash
python manage.py runserver 0.0.0.0:8000
```

---

# POR QUE 0.0.0.0?

Porque no Codespaces:

localhost sozinho não funciona corretamente externamente.

---

# 24 — SERIALIZERS

Arquivo:

```text
serializers.py
```

---

# O QUE É SERIALIZER?

Converte:

Python ↔ JSON

Também valida dados.

---

# EXEMPLO

```python
class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = '__all__'
```

---

# 25 — VIEWSETS

Arquivo:

```text
views.py
```

---

# O QUE É VIEWSET?

Controla:

- GET
- POST
- PUT
- PATCH
- DELETE

automaticamente.

---

# EXEMPLO

```python
class UsuarioViewSet(viewsets.ModelViewSet):

    queryset = Usuario.objects.all()

    serializer_class = UsuarioSerializer
```

---

# 26 — URLS

Arquivo:

```text
urls.py
```

---

# ROUTER

Usamos:

```python
DefaultRouter
```

---

# EXEMPLO

```python
router = DefaultRouter()

router.register(
    r'usuarios',
    UsuarioViewSet
)
```

---

# 27 — SWAGGER

# IMPORTS

```python
from drf_yasg.views import get_schema_view
```

---

# URLS

```python
path(
    'swagger/',
    schema_view.with_ui('swagger')
)

path(
    'redoc/',
    schema_view.with_ui('redoc')
)
```

---

# O QUE É SWAGGER?

Documentação interativa da API.

---

# O QUE É REDOC?

Outra documentação visual da API.

---

# 28 — FILTROS

# IMPORTS

```python
from django_filters.rest_framework import DjangoFilterBackend
```

---

# CONFIGURAÇÃO

```python
filter_backends = [
    DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter,
]
```

---

# FILTROS EXATOS

```python
filterset_fields = ['ativo']
```

---

# BUSCA TEXTUAL

```python
search_fields = ['nome']
```

---

# ORDENAÇÃO

```python
ordering_fields = ['nome']
```

---

# 29 — ENDPOINT PERSONALIZADO

Usar:

```python
@action(detail=True, methods=['get'])
```

---

# EXEMPLO

```python
@action(detail=True, methods=['get'])

def extrato(self, request, pk=None):

    usuario = self.get_object()

    return Response({
        'saldo': usuario.saldo
    })
```

---

# 30 — RELATÓRIOS

# IMPORTS IMPORTANTES

```python
from django.db.models import Count, Sum
```

---

# COUNT

Conta registros.

---

# SUM

Soma valores.

---

# AGGREGATE

Retorna cálculo geral.

---

# ANNOTATE

Adiciona campo calculado.

---

# DISTINCT

Remove repetidos.

---

# TRUNCDATE

Agrupa por dia.

```python
from django.db.models.functions import TruncDate
```

---

# 31 — ARQUIVO HTTP

Criar:

```text
api.http
```

---

# EXEMPLO GET

```http
GET http://localhost:8000/usuarios/
```

---

# EXEMPLO POST

```http
POST http://localhost:8000/usuarios/
Content-Type: application/json

{
    "nome": "Aaron"
}
```

---

# 32 — COMANDOS IMPORTANTES

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

# Instalar dependências

```bash
pip install -r requirements.txt
```

---

# 33 — CHECKLIST FINAL DA PROVA

```text
[ ] PostgreSQL funcionando
[ ] settings.py configurado
[ ] app criada
[ ] models
[ ] serializers
[ ] views
[ ] urls
[ ] migrations
[ ] swagger
[ ] filtros
[ ] relatórios
[ ] endpoints customizados
[ ] arquivo .http
[ ] CRUD funcionando
```

---

# DICAS FINAIS IMPORTANTES

# SEMPRE TESTAR:

- GET
- POST
- PUT
- PATCH
- DELETE

---

# SEMPRE VERIFICAR:

- migrations
- imports
- vírgulas
- parênteses
- urls

---

# SE DER ERRO:

# 1
Ler a ÚLTIMA linha.

---

# 2
Normalmente ela explica o problema real.

---

# 3
Verificar:

- imports
- nomes errados
- migrations
- settings.py

---

# FLUXO IDEAL DURANTE A PROVA

```text
Projeto
→ App
→ PostgreSQL
→ Settings
→ Models
→ Migrations
→ Serializers
→ Views
→ URLs
→ Swagger
→ Filtros
→ Relatórios
→ HTTP
→ Testes
```

---

# CONCLUSÃO

Se seguir este guia:

- consegue criar APIs REST rapidamente
- configura PostgreSQL
- resolve erros comuns
- usa Swagger
- implementa CRUD
- cria filtros
- cria relatórios
- trabalha no Codespaces sem sofrer
