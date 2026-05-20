# import necessário para validar o formato do CPF dos eleitores.
import re

from rest_framework import serializers

from .models import (
    Eleitor,
    Eleicao,
    Candidato,
    AptidaoEleitor,
    RegistroVotacao,
    Voto
)

# Serializador de Eleitor, representando a estrutura de dados para um eleitor, transformando o modelo Eleitor em um formato JSON para a API.
class EleitorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Eleitor

        fields = '__all__'

    def validate_cpf(self, value):

        padrao = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'

        if not re.match(padrao, value):

            raise serializers.ValidationError(
                'CPF invalido'
            )

        return value

# Serializador de Eleição, representando a estrutura de dados para uma eleição, transformando o modelo Eleicao em um formato JSON para a API.
class EleicaoSerializer(serializers.ModelSerializer):

    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    total_candidatos = serializers.SerializerMethodField()

    total_aptos = serializers.SerializerMethodField()

    class Meta:

        model = Eleicao

        fields = '__all__'


    def get_total_candidatos(self, obj):

        return obj.candidatos.count()


    def get_total_aptos(self, obj):

        return obj.aptos.count()

# Serializador de Candidato, representando a estrutura de dados para um candidato, transformando o modelo Candidato em um formato JSON para a API.
class CandidatoSerializer(serializers.ModelSerializer):

    eleicao_titulo = serializers.CharField(
        source='eleicao.titulo',
        read_only=True
    )

    class Meta:

        model = Candidato

        fields = '__all__'

    def validate_numero(self, value):

        if value == 0:

            raise serializers.ValidationError(
                'Numero 0 reservado'
            )

        return value

# Serializador de Aptidão do Eleitor, representando a estrutura de dados para a aptidão de um eleitor para votar em uma eleição específica, transformando o modelo AptidaoEleitor em um formato JSON para a API.
class AptidaoEleitorSerializer(serializers.ModelSerializer):

    eleitor_nome = serializers.CharField(
        source='eleitor.nome',
        read_only=True
    )

    eleicao_titulo = serializers.CharField(
        source='eleicao.titulo',
        read_only=True
    )

    class Meta:

        model = AptidaoEleitor

        fields = '__all__'

# Serializador de Registro de Votação, representando a estrutura de dados para o registro de um eleitor que votou em uma eleição específica, transformando o modelo RegistroVotacao em um formato JSON para a API.
class RegistroVotacaoSerializer(serializers.ModelSerializer):

    eleitor_nome = serializers.CharField(
        source='eleitor.nome',
        read_only=True
    )

    eleicao_titulo = serializers.CharField(
        source='eleicao.titulo',
        read_only=True
    )

    class Meta:

        model = RegistroVotacao

        fields = '__all__'

# Serializador de Voto, representando a estrutura de dados para um voto registrado em uma eleição, transformando o modelo Voto em um formato JSON para a API.
class VotoSerializer(serializers.ModelSerializer):

    candidato_nome_urna = serializers.CharField(
        source='candidato.nome_urna',
        read_only=True,
        allow_null=True
    )

    em_branco_display = serializers.SerializerMethodField()

    class Meta:

        model = Voto

        exclude = ['comprovante_hash']


    def get_em_branco_display(self, obj):

        if obj.em_branco:
            return 'BRANCO'

        return None

# Serializador de Votação, representando a estrutura de dados para o processo de votação, validando as regras de negócio para registrar um voto em uma eleição específica.
class VotacaoInputSerializer(serializers.Serializer):

    eleitor_id = serializers.IntegerField()

    eleicao_id = serializers.IntegerField()

    candidato_id = serializers.IntegerField(
        required=False
    )

    em_branco = serializers.BooleanField(
        default=False
    )

    def validate(self, data):

        try:

            eleicao = Eleicao.objects.get(
                id=data['eleicao_id']
            )

        except Eleicao.DoesNotExist:

            raise serializers.ValidationError(
                'Eleicao nao encontrada'
            )

        if eleicao.status != 'aberta':

            raise serializers.ValidationError(
                'Eleicao nao esta aberta'
            )

        eleitor = Eleitor.objects.get(
            id=data['eleitor_id']
        )

        apto = AptidaoEleitor.objects.filter(
            eleitor=eleitor,
            eleicao=eleicao
        ).exists()

        if not apto:

            raise serializers.ValidationError(
                'Eleitor nao esta apto'
            )

        ja_votou = RegistroVotacao.objects.filter(
            eleitor=eleitor,
            eleicao=eleicao
        ).exists()

        if ja_votou:

            raise serializers.ValidationError(
                'Eleitor ja votou'
            )

        candidato_id = data.get('candidato_id')

        em_branco = data.get('em_branco')

        if em_branco and candidato_id:

            raise serializers.ValidationError(
                'Escolha candidato OU branco'
            )

        if not em_branco and not candidato_id:

            raise serializers.ValidationError(
                'Informe candidato'
            )

        if candidato_id:

            candidato = Candidato.objects.filter(
                id=candidato_id,
                eleicao=eleicao
            ).exists()

            if not candidato:

                raise serializers.ValidationError(
                    'Candidato invalido'
                )

        return data