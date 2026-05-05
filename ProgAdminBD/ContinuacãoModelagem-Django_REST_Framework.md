# Continuação de Modelagem com Django REST Framework

Este material continua a modelagem inicial, adicionando entidades mais próximas de um cenário real de e-commerce.

## 1) Novos modelos

### Vendedor
Campos principais:
- `nome`
- `email` (único)
- `cpf` (único)
- `telefone`
- `salario`
- `ativo`
- `data_admissao`

### Produto
Campos principais:
- `nome`
- `preco`
- `estoque`
- `categoria`
- `disponivel`
- `data_criacao`
- `data_atualizacao`

## 2) Serializer dos novos recursos
Foram criados:
- `VendedorSerializer`
- `ProdutoSerializer`

Com `fields = '__all__'` para facilitar o CRUD completo.

## 3) ViewSets com recursos de consulta
Foram criados:
- `VendedorViewSet`
- `ProdutoViewSet`

Com suporte a:
- **Filtro** (`filterset_fields`)
- **Busca textual** (`search_fields`)
- **Ordenação** (`ordering_fields`)

## 4) Rotas automáticas
No `urls.py`, os viewsets estão registrados no router:
- `/amazon_api/vendedores/`
- `/amazon_api/produtos/`

## 5) Admin Django
Também foi configurado o `admin.py` para facilitar cadastro, busca e filtros internos pelo painel administrativo.

## 6) Resultado pedagógico
Com essa continuação, você pratica modelagem mais completa e aprende como expor recursos novos na API sem reescrever CRUD manualmente.