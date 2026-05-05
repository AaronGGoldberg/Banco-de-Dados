from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Cliente, Vendedor, Produto
from .serializers import ClienteSerializer, VendedorSerializer, ProdutoSerializer

# ViewSet para o modelo Cliente, utilizando ModelViewSet para fornecer os endpoints CRUD automaticamente.
class ClienteViewSet(viewsets.ModelViewSet):

    """
    ViewSet para o modelo Cliente.
    Fornece automaticamente os endpoints list, create, retrieve,
    update, partial_update e destroy.
    """

    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    # Habilita filtros, busca textual e ordenação via query params
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'email']
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'data_cadastro']

# ViewSets para Vendedor e Produto seguem a mesma estrutura, adaptando os campos de filtro, busca e ordenação conforme necessário.
class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'email', 'cpf', 'ativo']
    search_fields = ['nome', 'email', 'cpf']
    ordering_fields = ['nome', 'salario', 'data_admissao']

# ViewSet para o modelo Produto, com filtros específicos para categoria e disponibilidade.
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categoria', 'disponivel']
    search_fields = ['nome', 'categoria']
    ordering_fields = ['nome', 'preco', 'estoque', 'data_criacao']