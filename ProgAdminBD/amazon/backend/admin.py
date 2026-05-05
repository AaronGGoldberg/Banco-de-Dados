from django.contrib import admin
from .models import Cliente, Vendedor, Produto

# Registra o modelo Cliente no painel de administração do Django
@admin.register(Cliente)

# Define a classe de administração personalizada para o modelo Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'data_cadastro')
    search_fields = ('nome', 'email')
    ordering = ('nome',)

# Registra o modelo Vendedor no painel de administração do Django
@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'salario', 'ativo', 'data_admissao')
    list_filter = ('ativo',)
    search_fields = ('nome', 'email', 'cpf')
    ordering = ('nome',)

# Registra o modelo Produto no painel de administração do Django
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque', 'disponivel', 'data_criacao')
    list_filter = ('categoria', 'disponivel')
    search_fields = ('nome', 'categoria')
    ordering = ('nome',)