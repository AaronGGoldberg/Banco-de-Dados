# Sistema de Gerenciamento de Eleições

Aluno: Aaron Guerra Goldberg
Matrícula: 20251014040042

Projeto feito com Django REST Framework para a disciplina de PABD.

O sistema permite:
- cadastrar eleitores
- cadastrar eleições
- cadastrar candidatos
- registrar votos
- gerar comprovante
- gerar QR Code

---

# Como o anonimato do voto funciona

O sistema separa:
- quem votou
- em quem votou

A tabela RegistroVotacao guarda apenas o eleitor e a eleição.

A tabela Voto guarda apenas:
- eleição
- candidato
- data/hora
- hash do comprovante

A tabela Voto não possui ligação direta com Eleitor.

Assim o sistema consegue impedir voto duplicado sem revelar o voto do eleitor.

---

# Tecnologias usadas

- Python
- Django
- Django REST Framework
- PostgreSQL
- drf-yasg
- qrcode
- Pillow

---

# Instalação no Codespaces

Primeiro atualizar o sistema:

```bash
sudo apt update
```

Instalar PostgreSQL:

```bash
sudo apt install postgresql postgresql-contrib
```

Iniciar PostgreSQL:

```bash
sudo service postgresql start
```

Entrar no usuário postgres:

```bash
sudo su postgres
```

Abrir PostgreSQL:

```bash
psql
```

Criar banco:

```sql
CREATE DATABASE eleicoes_db;
```

Criar senha:

```sql
ALTER USER postgres WITH PASSWORD 'postgres';
```

Dar permissões:

```sql
GRANT ALL PRIVILEGES ON DATABASE eleicoes_db TO postgres;
```

Entrar no banco:

```sql
\c eleicoes_db
```

Dar permissão no schema public:

```sql
GRANT ALL ON SCHEMA public TO postgres;
```

Sair:

```sql
\q
```

Depois:

```bash
exit
```

---

# Criar ambiente virtual

```bash
python -m venv venv
```

Ativar:

Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

# Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Configuração do banco no settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eleicoes_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

# Migrações

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

# Criar superusuário

```bash
python manage.py createsuperuser
```

---

# Rodar servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

---

# Swagger

```text
/swagger/
```

---

# ReDoc

```text
/redoc/
```

---

# Endpoints principais

## Eleitores

```text
/eleicoes_api/eleitores/
```

## Eleições

```text
/eleicoes_api/eleicoes/
```

## Candidatos

```text
/eleicoes_api/candidatos/
```

## Registrar voto

```text
/eleicoes_api/eleicoes/{id}/votar/
```

## Verificar comprovante

```text
/eleicoes_api/verificar-comprovante/
```

---

# Funcionalidades implementadas

- CRUD de eleitores
- CRUD de eleições
- CRUD de candidatos
- CRUD de aptidões
- registro de votos
- voto em branco
- geração de QR Code
- verificação de comprovante
- Swagger
- ReDoc

---

# Diagrama

O diagrama do banco foi feito no dbdiagram.io e anexado ao projeto.

[Diagrama de Modelo de Dados - dbdiagram.io](DiagramaModeloDados.png)