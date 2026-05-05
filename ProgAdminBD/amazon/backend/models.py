from django.db import models

# Create your models here.


class Cliente(models.Model):

    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    telefone = models.CharField(max_length=20, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    
    class Meta:
        db_table = 'clientes'
        ordering = ['nome']
    
    def __str__(self):
        return f'{self.nome} <{self.email}>'
    
from django.db import models

# Create your models here.


class Cliente(models.Model):

    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False) # UNIQUE no banco
    email = models.EmailField(unique=True, null=False, blank=False)
    telefone = models.CharField(max_length=20, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=False, blank=False) # Preenchido automaticamente
    
    data_cadastro = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        db_table = 'clientes' # Nome explícito da tabela no banco
        ordering = ['nome'] # Ordenação padrão nas consultas
    
        db_table = 'clientes'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} <{self.email}>'


class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    data_admissao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendedores'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    categoria = models.CharField(max_length=100)
    disponivel = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome