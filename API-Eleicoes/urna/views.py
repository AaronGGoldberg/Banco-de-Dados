from django.shortcuts import render
from django.urls import reverse
import hashlib
import secrets
from io import BytesIO

import qrcode

from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Eleitor,
    Eleicao,
    Candidato,
    AptidaoEleitor,
    RegistroVotacao,
    Voto
)

from .serializers import (
    EleitorSerializer,
    EleicaoSerializer,
    CandidatoSerializer,
    AptidaoEleitorSerializer,
    RegistroVotacaoSerializer,
    VotoSerializer,
    VotacaoInputSerializer
)

# Views para os endpoints da API, utilizando viewsets do Django REST Framework para criar as operações CRUD para o modelo Eleitor.
class EleitorViewSet(viewsets.ModelViewSet):

    queryset = Eleitor.objects.all()

    serializer_class = EleitorSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]

    filterset_fields = ['ativo']

    search_fields = ['nome', 'email', 'cpf']

# Views para os endpoints da API, utilizando viewsets do Django REST Framework para criar as operações CRUD para o modelo Eleicao.
class EleicaoViewSet(viewsets.ModelViewSet):

    queryset = Eleicao.objects.all()

    serializer_class = EleicaoSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['status', 'tipo']

    search_fields = ['titulo']

    ordering_fields = ['data_inicio']


    @action(detail=True, methods=['post'])

    def abrir(self, request, pk=None):

        eleicao = self.get_object()

        if eleicao.status != 'rascunho':

            return Response(
                {'erro': 'Eleicao invalida'},
                status=400
            )

        if eleicao.candidatos.count() < 2:

            return Response(
                {'erro': 'Poucos candidatos'},
                status=400
            )

        if eleicao.aptos.count() < 1:

            return Response(
                {'erro': 'Sem eleitores aptos'},
                status=400
            )

        eleicao.status = 'aberta'

        eleicao.save()

        serializer = self.get_serializer(eleicao)

        return Response(serializer.data)


    @action(detail=True, methods=['post'])

    def encerrar(self, request, pk=None):

        eleicao = self.get_object()

        eleicao.status = 'encerrada'

        eleicao.save()

        return Response({
            'mensagem': 'Eleicao encerrada'
        })


    @action(detail=True, methods=['post'])

    def votar(self, request, pk=None):

        dados = request.data.copy()

        dados['eleicao_id'] = pk

        serializer = VotacaoInputSerializer(
            data=dados
        )

        serializer.is_valid(raise_exception=True)

        dados = serializer.validated_data

        eleitor = Eleitor.objects.get(
            id=dados['eleitor_id']
        )

        eleicao = Eleicao.objects.get(id=pk)

        try:

            RegistroVotacao.objects.create(
                eleitor=eleitor,
                eleicao=eleicao
            )

        except:

            return Response(
                {'erro': 'Eleitor ja votou'},
                status=409
            )

        token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(
            token.encode()
        ).hexdigest()

        candidato = None

        if dados.get('candidato_id'):

            candidato = Candidato.objects.get(
                id=dados['candidato_id']
            )

        voto = Voto.objects.create(
            eleicao=eleicao,
            candidato=candidato,
            em_branco=dados.get('em_branco'),
            comprovante_hash=token_hash
        )

        candidato_nome = 'BRANCO'

        if candidato:
            candidato_nome = candidato.nome_urna

        return Response({

            'mensagem': 'Voto registrado',

            'comprovante': {

                'token': token,

                'eleicao': eleicao.titulo,

                'candidato': candidato_nome,

                'data_hora': voto.data_hora,

                'qr_code_url': request.build_absolute_uri(f'/eleicoes_api/comprovantes/qr/?token={token}')
            }

        }, status=201)

# Views para os endpoints da API, utilizando viewsets do Django REST Framework para criar as operações CRUD para o modelo Candidato.
class CandidatoViewSet(viewsets.ModelViewSet):

    queryset = Candidato.objects.select_related(
        'eleicao'
    )

    serializer_class = CandidatoSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]

    filterset_fields = ['eleicao']

    search_fields = [
        'nome',
        'nome_urna',
        'partido_ou_chapa'
    ]

# Views para os endpoints da API, utilizando viewsets do Django REST Framework para criar as operações CRUD para o modelo AptidaoEleitor.
class AptidaoEleitorViewSet(viewsets.ModelViewSet):

    queryset = AptidaoEleitor.objects.select_related(
        'eleitor',
        'eleicao'
    )

    serializer_class = AptidaoEleitorSerializer

    filter_backends = [
        DjangoFilterBackend
    ]

    filterset_fields = [
        'eleitor',
        'eleicao'
    ]

# Views para os endpoints da API, utilizando viewsets do Django REST Framework para criar as operações CRUD para o modelo RegistroVotacao.
class RegistroVotacaoViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = RegistroVotacao.objects.all().order_by(
        '-data_hora'
    )

    serializer_class = RegistroVotacaoSerializer

    filter_backends = [
        DjangoFilterBackend
    ]

    filterset_fields = ['eleicao']

# Views para os endpoints da API, utilizando viewsets do Django REST Framework para criar as operações CRUD para o modelo Voto.
class VotoViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Voto.objects.all()

    serializer_class = VotoSerializer

    filter_backends = [
        DjangoFilterBackend
    ]

    filterset_fields = ['eleicao']


@api_view(['GET'])

def verificar_comprovante(request):

    token = request.GET.get('token')

    if not token:
        return Response({
            'valido': False,
            'mensagem': 'Token não fornecido'
        }, status=400)

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    try:

        voto = Voto.objects.get(
            comprovante_hash=token_hash
        )

        candidato = 'BRANCO'

        if voto.candidato:
            candidato = voto.candidato.nome_urna

        return Response({

            'valido': True,

            'eleicao': voto.eleicao.titulo,

            'candidato': candidato,

            'data_hora': voto.data_hora
        })

    except:

        return Response({

            'valido': False,

            'mensagem': 'Comprovante invalido'

        }, status=404)


@api_view(['GET'])

def gerar_qrcode(request):

    token = request.GET.get('token')

    if not token:
        return Response({
            'erro': 'Token não fornecido'
        }, status=400)

    verify_path = reverse('verificar-comprovante')
    url = request.build_absolute_uri(f'{verify_path}?token={token}')

    img = qrcode.make(url)

    buffer = BytesIO()

    img.save(buffer, format='PNG')

    return HttpResponse(
        buffer.getvalue(),
        content_type='image/png'
    )