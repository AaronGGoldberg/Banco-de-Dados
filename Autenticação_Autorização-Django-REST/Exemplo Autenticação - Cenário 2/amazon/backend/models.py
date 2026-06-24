from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class Usuario(AbstractUser):
    class Tipo(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        VENDEDOR = 'VENDEDOR', 'Vendedor'
    
    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices,
        default=Tipo.CLIENTE,
    )
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=15, blank=True)
    
    def is_cliente(self):
        return self.tipo == self.Tipo.CLIENTE
    
    def is_vendedor(self):
        return self.tipo == self.Tipo.VENDEDOR
    
    def __str__(self):
        return f'{self.username} ({self.get_tipo_display()})'

class Cliente(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='cliente',
        null=True
    )
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    endereco_entrega = models.CharField(max_length=255, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.usuario.email} - {self.cpf} - {self.endereco_entrega} - {self.data_nascimento}'

class Vendedor(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vendedor',
        null=True
    )
    nome_loja = models.CharField(max_length=255, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=14, unique=True)
    avaliacao = models.DecimalField(max_digits=3, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.usuario.email} - {self.cpf_cnpj} - {self.avaliacao} - {self.ativo}'

class Produto(models.Model):
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.PROTECT, #nao pode deletar um vendedor que tem produtos
        related_name='produtos',
        null=True,
        blank=True
    ) 
    nome = models.CharField(max_length=255, null=False, blank=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    descricao = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.preco} - {self.data_cadastro}'

class PerfilVendedor(models.Model):
    vendedor = models.OneToOneField(
        Vendedor,
        on_delete=models.CASCADE,
        related_name='perfil',
        primary_key=True
    )

    razao_social = models.CharField(max_length=150, blank=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True)
    banco = models.CharField(max_length=50, blank=True)
    agencia = models.CharField(max_length=10, blank=True)
    conta = models.CharField(max_length=20, blank=True)
    chave_pix = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Perfil de {self.vendedor.nome}'

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos'
    ) 
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )
    data_pedido = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f'Pedido #{self.id} de {self.cliente.nome} - Status: {self.status}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE, #pode deletar um pedido mesmo que ele tenha itens
        related_name='itens'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT, #nao pode deletar um produto que esta em um pedido
        related_name='itens_pedido'
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2) # o preco unitario nao pode ser alterado


    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome} em #{self.pedido.id}'

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
        