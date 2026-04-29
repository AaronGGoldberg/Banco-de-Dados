from rest_framework import viewsets
from .models import Cliente, Vendedor, Produto, PerfilVendedor, Pedido, ItemPedido
from .serializers import ClienteSerializer, VendedorSerializer, ProdutoSerializer, PerfilVendedorSerializer, PedidoSerializer, ItemPedidoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class PerfilVendedorViewSet(viewsets.ModelViewSet):
    queryset = PerfilVendedor.objects.select_related('vendedor').all()
    serializer_class = PerfilVendedorSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    def get_queryset(self):
        return (Pedido.objects
                .select_related('cliente')
                .prefetch_related('itens__produto')
                .all())

class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.select_related('pedido', 'produto').all()
    serializer_class = ItemPedidoSerializer
    


