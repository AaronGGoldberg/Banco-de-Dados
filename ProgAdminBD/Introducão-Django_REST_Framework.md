# Introdução ao Django REST Framework

## 1) Ideia geral
O Django REST Framework (DRF) é uma biblioteca do Django para criar APIs REST de forma rápida.

Em vez de retornar HTML, a API devolve **JSON**. Isso facilita integração com front-end (React/Vue), apps mobile e outros sistemas.

## 2) Estrutura mínima
No projeto desta pasta (`amazon`), os blocos principais são:

- `models.py`: define as tabelas (ORM)
- `serializers.py`: converte Model ↔ JSON
- `views.py`: define regras de endpoint (CRUD)
- `urls.py`: registra rotas

## 3) Fluxo básico de uma requisição
1. Cliente chama endpoint (`GET/POST/PUT/PATCH/DELETE`)
2. ViewSet recebe requisição
3. Serializer valida e transforma dados
4. Model salva/consulta no banco
5. API responde em JSON

## 4) Recursos do DRF usados aqui
- `ModelSerializer`
- `ModelViewSet`
- `DefaultRouter`
- `DjangoFilterBackend`
- `SearchFilter`
- `OrderingFilter`

## 5) Endpoints atuais
- `/amazon_api/clientes/`
- `/amazon_api/vendedores/`
- `/amazon_api/produtos/`

## 6) Dica prática
Sempre teste primeiro no Swagger (`/swagger/`) porque ele já mostra os campos esperados em cada endpoint.