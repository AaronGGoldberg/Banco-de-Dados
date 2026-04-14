from django.contrib import admin
from .models import Cliente

# Registra o modelo Cliente no painel de administração do Django
@admin.register(Cliente)

# Define a classe de administração personalizada para o modelo Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'data_cadastro') # Campos a serem exibidos na lista de clientes
    search_fields = ('nome', 'email') # Campos que podem ser pesquisados no painel de administração
    ordering = ('nome',) # Ordenação padrão por nome
