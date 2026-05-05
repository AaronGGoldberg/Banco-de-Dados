# Relacionamento entre Modelos (guia para próxima etapa)

> Situação atual: os modelos estão independentes (`Cliente`, `Vendedor`, `Produto`).
> Próxima evolução: criar relacionamentos entre eles.

## 1) Tipos de relacionamento mais usados

### 1.1 OneToOneField (1:1)
Um registro se conecta a apenas um outro registro.
Exemplo: `PerfilVendedor` ligado a um `Vendedor`.

### 1.2 ForeignKey (N:1)
Muitos registros apontam para um registro “pai”.
Exemplo: vários `Produto` podem apontar para um único `Vendedor`.

### 1.3 ManyToManyField (N:N)
Muitos com muitos.
Exemplo clássico: `Pedido` com vários `Produto`, e um `Produto` em vários `Pedido`.

## 2) Exemplo de evolução sugerida

### Produto ligado a Vendedor (ForeignKey)
No `Produto`, adicionar:

```python
vendedor = models.ForeignKey(
    'Vendedor',
    on_delete=models.PROTECT,
    related_name='produtos'
)
```

- `PROTECT` evita apagar vendedor com produtos ativos.
- `related_name='produtos'` permite fazer `vendedor.produtos.all()`.

## 3) Fluxo recomendado em sala
1. Ajustar `models.py`
2. Rodar `makemigrations` e `migrate`
3. Ajustar serializers (se necessário)
4. Testar no Swagger
5. Testar filtros por relacionamento

## 4) Cuidados importantes
- Defina `on_delete` com intenção de negócio.
- Evite apagar dados críticos sem regra clara.
- Use nomes de campos intuitivos para facilitar manutenção.

## 5) Ganho prático
Com relacionamentos, a API representa melhor o mundo real e permite consultas mais úteis (ex.: listar produtos de um vendedor específico).