from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from django.utils import timezone
from datetime import timedelta

from django.db.models import Count

from django.db.models.functions import TruncDate

from decimal import Decimal, InvalidOperation

from .models import (
    Municipio,
    EmpresaTransporte,
    Usuario,
    TipoTicket,
    Ticket,
    Transporte,
    Validador,
    Validacao
)

from .serializers import (
    MunicipioSerializer,
    EmpresaTransporteSerializer,
    UsuarioSerializer,
    TipoTicketSerializer,
    TicketSerializer,
    TransporteSerializer,
    ValidadorSerializer,
    ValidacaoSerializer
)

class MunicipioViewSet(viewsets.ModelViewSet):

    queryset = Municipio.objects.all()

    serializer_class = MunicipioSerializer

    filter_backends = [
        SearchFilter
    ]

    search_fields = [
        'nome'
    ]

    @action(detail=True, methods=['get'])

    def relatorio_geral(self, request, pk=None):

        municipio = self.get_object()

        data_limite = timezone.now() - timedelta(days=30)

        empresas = EmpresaTransporte.objects.filter(
            municipio=municipio
        )

        transportes = Transporte.objects.filter(
            empresa__municipio=municipio,
            ativo=True
        )

        tickets = Ticket.objects.filter(
            usuario__municipio=municipio,
            data_compra__gte=data_limite
        )

        validacoes = Validacao.objects.filter(
            transporte__empresa__municipio=municipio,
            data_hora__gte=data_limite
        )

        empresas_total = empresas.count()

        transportes_por_tipo = transportes.values(
            'tipo'
        ).annotate(
            total=Count('id')
        )

        tickets_por_tipo = tickets.values(
            'tipo__nome'
        ).annotate(
            total=Count('id')
        )

        receita_total = validacoes.aggregate(
            total=Sum('valor_debitado')
        )['total'] or 0

        total_validacoes = validacoes.count()

        dados = {

            'municipio': {
                'id': municipio.id,
                'nome': municipio.nome,
                'uf': municipio.uf
            },

            'empresas_concedidas': empresas_total,

            'transportes_ativos_por_tipo': list(
                transportes_por_tipo
            ),

            'tickets_vendidos_ultimo_mes': list(
                tickets_por_tipo
            ),

            'receita_total_ultimo_mes': receita_total,

            'validacoes_ultimo_mes': total_validacoes
        }

        return Response(dados)

class EmpresaTransporteViewSet(viewsets.ModelViewSet):

    queryset = EmpresaTransporte.objects.all()

    serializer_class = EmpresaTransporteSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter
    ]

    filterset_fields = [
        'municipio'
    ]

    search_fields = [
        'razao_social',
        'nome_fantasia',
        'cnpj'
    ]

    @action(detail=True, methods=['get'])

    def relatorio(self, request, pk=None):

        empresa = self.get_object()

        transportes = Transporte.objects.filter(
            empresa=empresa
        )

        validacoes = Validacao.objects.filter(
            transporte__empresa=empresa
        )

        dados = {
            'empresa': empresa.nome_fantasia,
            'quantidade_transportes': transportes.count(),
            'quantidade_validacoes': validacoes.count(),
        }

        return Response(dados)
    
    @action(detail=True, methods=['get'])

    def painel(self, request, pk=None):

        empresa = self.get_object()

        data_limite = timezone.now() - timedelta(days=30)

        transportes = Transporte.objects.filter(
            empresa=empresa,
            ativo=True
        )

        validadores = Validador.objects.filter(
            ativo=True,
            transporte__empresa=empresa
        )

        validacoes_30d = Validacao.objects.filter(
            transporte__empresa=empresa,
            data_hora__gte=data_limite
        )

        transportes_por_tipo = transportes.values(
            'tipo'
        ).annotate(
            total=Count('id')
        )

        validadores_por_tipo = validadores.values(
            'tipo'
        ).annotate(
            total=Count('id')
        )

        top_transportes = validacoes_30d.values(
            'transporte__id',
            'transporte__nome',
            'transporte__identificacao'
        ).annotate(
            total_validacoes=Count('id')
        ).order_by(
            '-total_validacoes'
        )[:5]

        validacoes_por_dia = validacoes_30d.annotate(
            dia=TruncDate('data_hora')
        ).values(
            'dia'
        ).annotate(
            total=Count('id')
        ).order_by('dia')

        dados = {

            'empresa': {
                'id': empresa.id,
                'nome_fantasia': empresa.nome_fantasia,
                'cnpj': empresa.cnpj
            },

            'transportes_ativos_por_tipo': list(
                transportes_por_tipo
            ),

            'validadores_ativos_por_tipo': list(
                validadores_por_tipo
            ),

            'top_5_transportes': list(
                top_transportes
            ),

            'validacoes_ultimos_30_dias': list(
                validacoes_por_dia
            )
        }

        return Response(dados)

class UsuarioViewSet(viewsets.ModelViewSet):

    queryset = Usuario.objects.all()

    serializer_class = UsuarioSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        'nome',
        'email',
        'cpf'
    ]

    ordering_fields = [
        'data_cadastro'
    ]

    @action(detail=True, methods=['get'])

    def extrato(self, request, pk=None):

        usuario = self.get_object()

        data_limite = timezone.now() - timedelta(days=30)

        tickets = Ticket.objects.filter(
            usuario=usuario
        )

        validacoes = Validacao.objects.filter(
            ticket__usuario=usuario
        )

        validacoes_30d = validacoes.filter(
            data_hora__gte=data_limite
        )

        tickets_ativos = tickets.filter(
            status='ativo'
        ).count()

        tickets_expirados = tickets.filter(
            status='expirado'
        ).count()

        valor_total_gasto = tickets.aggregate(
            total=Sum('valor_pago')
        )['total'] or 0

        valor_economizado = validacoes.filter(
            dentro_janela_integracao=True
        ).count()

        valor_economizado *= 4

        dados = {

            'usuario': usuario.nome,

            'cpf': usuario.cpf,

            'saldo_atual': usuario.saldo,

            'tickets_comprados': tickets.count(),

            'tickets_ativos': tickets_ativos,

            'tickets_expirados': tickets_expirados,

            'validacoes_realizadas': validacoes.count(),

            'validacoes_30d': validacoes_30d.count(),

            'valor_total_gasto': valor_total_gasto,

            'valor_economizado_integracao':
                valor_economizado
        }

        return Response(dados)

    @action(detail=True, methods=['post'])

    def recarregar(self, request, pk=None):

        usuario = self.get_object()

        valor = request.data.get('valor')

        if not valor:
            return Response(
                {'erro': 'Informe o valor'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            valor = Decimal(str(valor))
        except (InvalidOperation, TypeError, ValueError):
            return Response(
                {'erro': 'Valor inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if valor <= 0:
            return Response(
                {'erro': 'Valor inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario.saldo += valor

        usuario.save()

        return Response({
            'mensagem': 'Recarga realizada',
            'novo_saldo': usuario.saldo
        })        

class TipoTicketViewSet(viewsets.ModelViewSet):

    queryset = TipoTicket.objects.all()

    serializer_class = TipoTicketSerializer

    filter_backends = [
        DjangoFilterBackend
    ]

    filterset_fields = [
        'nome',
        'ativo'
    ]

class TicketViewSet(viewsets.ModelViewSet):

    queryset = Ticket.objects.select_related(
        'usuario',
        'tipo'
    )

    serializer_class = TicketSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_fields = [
        'usuario',
        'tipo',
        'status'
    ]

    ordering_fields = [
        'data_compra'
    ]

    @action(detail=True, methods=['post'])

    def validar(self, request, pk=None):

        ticket = self.get_object()

        if ticket.status != 'ativo':

            return Response(
                {
                    'erro': 'Ticket inválido ou expirado'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validador_id = request.data.get('validador_id')

        transporte_id = request.data.get('transporte_id')

        if not validador_id or not transporte_id:

            return Response(
                {
                    'erro': 'Informe validador_id e transporte_id'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            validador = Validador.objects.get(
                id=validador_id
            )

            transporte = Transporte.objects.get(
                id=transporte_id
            )

        except:

            return Response(
                {
                    'erro': 'Validador ou transporte inválido'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario = ticket.usuario

        tipo = ticket.tipo

        agora = timezone.now()

        janela_inicio = agora - timedelta(
            minutes=tipo.janela_integracao_minutos
        )

        ultima_validacao = Validacao.objects.filter(
            ticket__usuario=usuario,
            data_hora__gte=janela_inicio
        ).order_by('-data_hora').first()

        dentro_integracao = ultima_validacao is not None

        valor_debitado = 0

        mensagem = ''

        if dentro_integracao:

            mensagem = 'Integração tarifária'

        else:

            valor_debitado = tipo.valor

            if usuario.saldo < valor_debitado:

                return Response(
                    {
                        'erro': 'Saldo insuficiente'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            usuario.saldo -= valor_debitado

            usuario.save()

            mensagem = 'Nova passagem'

        validacao = Validacao.objects.create(
            ticket=ticket,
            validador=validador,
            transporte=transporte,
            dentro_janela_integracao=dentro_integracao,
            valor_debitado=valor_debitado
        )

        if (
            tipo.nome.lower() == 'avulso'
            and
            not dentro_integracao
        ):

            ticket.status = 'consumido'

            ticket.save()

        dados = ValidacaoSerializer(validacao).data

        dados['mensagem'] = mensagem

        return Response(
            dados,
            status=status.HTTP_201_CREATED
        )

class TransporteViewSet(viewsets.ModelViewSet):

    queryset = Transporte.objects.all()

    serializer_class = TransporteSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter
    ]

    filterset_fields = [
        'tipo',
        'empresa',
        'ativo'
    ]

    search_fields = [
        'identificacao',
        'nome'
    ]

    @action(detail=True, methods=['get'])

    def relatorio(self, request, pk=None):

        transporte = self.get_object()

        inicio = request.query_params.get('inicio')

        fim = request.query_params.get('fim')

        validacoes = Validacao.objects.filter(
            transporte=transporte
        )

        if inicio:

            validacoes = validacoes.filter(
                data_hora__date__gte=inicio
            )

        if fim:

            validacoes = validacoes.filter(
                data_hora__date__lte=fim
            )

        total_validacoes = validacoes.count()

        usuarios_unicos = validacoes.values(
            'ticket__usuario'
        ).distinct().count()

        distribuicao = validacoes.values(
            'ticket__tipo__nome'
        ).annotate(
            total=Count('id')
        )

        receita = validacoes.aggregate(
            total=Sum('valor_debitado')
        )['total'] or 0

        dados = {
            'transporte': {
                'id': transporte.id,
                'identificacao': transporte.identificacao,
                'tipo': transporte.tipo,
                'nome': transporte.nome,
                'empresa': transporte.empresa.nome_fantasia
            },

            'periodo': {
                'inicio': inicio,
                'fim': fim
            },

            'total_validacoes': total_validacoes,

            'usuarios_unicos': usuarios_unicos,

            'distribuicao_por_tipo_ticket': list(distribuicao),

            'receita_total': receita
        }

        return Response(dados)    

class ValidadorViewSet(viewsets.ModelViewSet):

    queryset = Validador.objects.all()

    serializer_class = ValidadorSerializer

    filter_backends = [
        DjangoFilterBackend
    ]

    filterset_fields = [
        'tipo',
        'transporte',
        'ativo'
    ]

class ValidacaoViewSet(viewsets.ModelViewSet):

    queryset = Validacao.objects.select_related(
        'ticket__usuario',
        'ticket__tipo',
        'validador',
        'transporte'
    )

    serializer_class = ValidacaoSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_fields = [
        'ticket',
        'validador',
        'transporte',
        'dentro_janela_integracao'
    ]

    ordering_fields = [
        'data_hora'
    ]
