from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Cliente
from .serializers import ClienteSerializer

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
    filterset_fields = ['nome', 'email'] # ?nome=Maria
    search_fields = ['nome', 'email'] # ?search=Maria
    ordering_fields = ['nome', 'data_cadastro'] # ?ordering=-data_cadastro