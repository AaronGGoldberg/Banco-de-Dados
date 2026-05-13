from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

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

class MunicipioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Municipio
        fields = '__all__'

class EmpresaTransporteSerializer(serializers.ModelSerializer):

    municipio_nome = serializers.CharField(
        source='municipio.nome',
        read_only=True
    )

    class Meta:
        model = EmpresaTransporte
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ['saldo']

class TipoTicketSerializer(serializers.ModelSerializer):

    nome_display = serializers.CharField(
        source='get_nome_display',
        read_only=True
    )

    class Meta:
        model = TipoTicket
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):

    usuario_nome = serializers.CharField(
        source='usuario.nome',
        read_only=True
    )

    tipo_nome = serializers.CharField(
        source='tipo.get_nome_display',
        read_only=True
    )

    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = '__all__'

        read_only_fields = [
            'valor_pago',
            'data_validade'
        ]

class TransporteSerializer(serializers.ModelSerializer):

    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )

    empresa_nome = serializers.CharField(
        source='empresa.nome_fantasia',
        read_only=True
    )

    class Meta:
        model = Transporte
        fields = '__all__'

class ValidadorSerializer(serializers.ModelSerializer):

    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )

    transporte_identificacao = serializers.CharField(
        source='transporte.identificacao',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Validador
        fields = '__all__'

class ValidacaoSerializer(serializers.ModelSerializer):

    usuario_nome = serializers.CharField(
        source='ticket.usuario.nome',
        read_only=True
    )

    tipo_ticket = serializers.CharField(
        source='ticket.tipo.get_nome_display',
        read_only=True
    )

    transporte_nome = serializers.CharField(
        source='transporte.nome',
        read_only=True
    )

    mensagem = serializers.SerializerMethodField()

    class Meta:
        model = Validacao
        fields = '__all__'

    def get_mensagem(self, obj):

        if obj.dentro_janela_integracao:
            return 'Integração tarifária'

        return 'Nova passagem'
    
    def create(self, validated_data):

        ticket = validated_data['ticket']

        usuario = ticket.usuario

        tipo_ticket = ticket.tipo

        if ticket.status != 'ativo':
            raise serializers.ValidationError(
                'Ticket inválido ou expirado'
            )

        janela_tempo = timezone.now() - timedelta(
            minutes=tipo_ticket.janela_integracao_minutos
        )

        ultima_validacao = Validacao.objects.filter(
            ticket__usuario=usuario,
            data_hora__gte=janela_tempo
        ).exists()

        if ultima_validacao:

            validated_data['dentro_janela_integracao'] = True
            validated_data['valor_debitado'] = 0

        else:

            if usuario.saldo < tipo_ticket.valor:
                raise serializers.ValidationError(
                    'Saldo insuficiente'
                )

            usuario.saldo -= tipo_ticket.valor
            usuario.save()

            validated_data['dentro_janela_integracao'] = False
            validated_data['valor_debitado'] = tipo_ticket.valor

            if tipo_ticket.nome == 'avulso':
                ticket.status = 'consumido'
                ticket.save()

        return super().create(validated_data)
    