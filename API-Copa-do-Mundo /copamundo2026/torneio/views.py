from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Grupo, Tecnico, Selecao, Jogador, Jogo, EventoJogo
from .serializers import GrupoSerializer, TecnicoSerializer, SelecaoSerializer, JogadorSerializer, JogoSerializer, EventoJogoSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

class TecnicoViewSet(viewsets.ModelViewSet):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

class SelecaoViewSet(viewsets.ModelViewSet):
    queryset = Selecao.objects.all()
    serializer_class = SelecaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['grupo']
    search_fields = ['nome', 'sigla']

class JogadorViewSet(viewsets.ModelViewSet):
    queryset = Jogador.objects.select_related('selecao').all()
    serializer_class = JogadorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['selecao', 'posicao', 'suspenso']
    search_fields = ['nome', 'nome_guerra']
    ordering_fields = ['selecao', 'numero_camisa']

class JogoViewSet(viewsets.ModelViewSet):
    queryset = (
        Jogo.objects
        .select_related('selecao_mandante', 'selecao_visitante', 'grupo')
        .prefetch_related('eventos__jogador')
        .all()
    )
    serializer_class = JogoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['fase', 'status', 'grupo']
    search_fields = ['estadio', 'cidade']
    ordering_fields = ['data_hora']

class EventoJogoViewSet(viewsets.ModelViewSet):
    queryset = EventoJogo.objects.select_related('jogo', 'jogador').all()
    serializer_class = EventoJogoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['jogo', 'jogador', 'tipo']
