from django.db import transaction
from rest_framework import serializers
from .models import (Usuario, Cliente, Vendedor, Produto, PerfilVendedor, Pedido, ItemPedido)

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
      
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password',
                'tipo', 'cpf', 'telefone']

    def create(self, validated_data):
        # create_user faz o hash da senha corretamente
        senha = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(senha)
        usuario.save()
        return usuario
 
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['cpf', 'endereco_entrega', 'data_nascimento']

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ['nome_loja', 'cpf_cnpj', 'avaliacao', 'ativo']

class RegistroSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True)

    # Os dois perfis são opcionais; o cliente envia apenas o seu
    cliente = ClienteSerializer(required=False)
    vendedor = VendedorSerializer(required=False)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'tipo',
        'telefone', 'cliente', 'vendedor']
        
    def validate(self, data):
        tipo = data.get('tipo')
        if tipo == Usuario.Tipo.CLIENTE and 'cliente' not in data:
            raise serializers.ValidationError(
            'Usuario precisa ter perfil cliente.')
        if tipo == Usuario.Tipo.VENDEDOR and 'vendedor' not in data:
            raise serializers.ValidationError(
                    'Usuario precisa ter perfil vendedor.')
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        dados_cliente = validated_data.pop('cliente', None)
        dados_vendedor = validated_data.pop('vendedor', None)
        senha = validated_data.pop('password')

        usuario = Usuario(**validated_data)
        usuario.set_password(senha)
        usuario.save()
        if dados_cliente:
            Cliente.objects.create(usuario=usuario, **dados_cliente)
        if dados_vendedor:
            Vendedor.objects.create(usuario=usuario, **dados_vendedor)
        return usuario
        

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class PerfilVendedorSerializer(serializers.ModelSerializer):
    vendedor_id = serializers.IntegerField(source='vendedor.id')    
    vendedor_nome = serializers.CharField(source='vendedor.nome', read_only=True) 
    
    def validate(self, attrs):
        vendedor_data = attrs.get('vendedor', {})
        vendedor_id = vendedor_data.get('id') if isinstance(vendedor_data, dict) else None
        if vendedor_id is None:
            raise serializers.ValidationError({'vendedor_id': 'Este campo é obrigatório.'})
        try:
            attrs['vendedor'] = Vendedor.objects.get(id=vendedor_id)
        except Vendedor.DoesNotExist:
            raise serializers.ValidationError({'vendedor_id': f'Vendedor com id={vendedor_id} não encontrado.'})
        return attrs

    class Meta:
        model = PerfilVendedor
        fields = ['vendedor_id', 'vendedor_nome', 'razao_social','inscricao_estadual', 'banco', 'agencia','conta', 'chave_pix']
    
class ItemPedidoSerializer(serializers.ModelSerializer):

    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_id = serializers.IntegerField(source='produto.id')
    preco_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def validate(self, attrs):
        if 'produto' not in attrs:
            return attrs
        produto_data = attrs['produto']
        produto_id = produto_data.get('id') if isinstance(produto_data, dict) else None
        if produto_id is None:
            raise serializers.ValidationError({'produto_id': 'Este campo é obrigatório.'})
        try:
            attrs['produto'] = Produto.objects.get(id=produto_id)
        except Produto.DoesNotExist:
            raise serializers.ValidationError({'produto_id': f'Produto com id={produto_id} não encontrado.'})
        return attrs

    class Meta:
        model = ItemPedido
        fields = ['id', 'pedido', 'produto_id', 'produto_nome', 'quantidade', 'preco_unitario', 'subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cliente_nome', 'status', 'data_pedido', 'observacoes', 'itens', 'total']
        read_only_fields = ['data_pedido']

    def get_total(self, obj):
        return sum(i.quantidade * i.preco_unitario for i in obj.itens.all())

    def create(self, validated_data):
        itens_data = validated_data.pop('itens', [])
        pedido = Pedido.objects.create(**validated_data)
        for item_data in itens_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)
        return pedido

    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens', None)
        # Atualiza campos do pedido
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Substitui completamente os itens, se enviados
        if itens_data is not None:
            instance.itens.all().delete()
            for item_data in itens_data:
                ItemPedido.objects.create(pedido=instance, **item_data)
        return instance 

