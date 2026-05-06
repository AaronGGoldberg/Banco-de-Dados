from rest_framework import serializers
from .models import Grupo, Tecnico, Selecao, Jogador, Jogo, EventoJogo

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'

class TecnicoSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Tecnico
        fields = '__all__'

class SelecaoSerializer(serializers.ModelSerializer):
    tecnico_nome = serializers.CharField(source='tecnico.nome', read_only=True)

    class Meta:
        model = Selecao
        fields = '__all__'

class JogadorSerializer(serializers.ModelSerializer):
    posicao_display = serializers.CharField(source='get_posicao_display', read_only=True)
    class Meta:
        model = Jogador
        fields = '__all__'

class EventoJogoSerializer(serializers.ModelSerializer):
    jogador_nome = serializers.CharField(source='jogador.nome_guerra', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = EventoJogo
        fields = '__all__'
    
    def create(self, validated_data):
        evento = EventoJogo.objects.create(**validated_data)
        if evento.tipo == 'GOL':
            if evento.jogo.selecao_mandante == evento.jogador.selecao:
                evento.jogo.gols_mandante += 1
            else:
                evento.jogo.gols_visitante += 1                              
        evento.jogo.save()
        return evento

    def update(self, instance, validated_data):
        if self.validated_data['tipo'] == 'GOL':
            if instance.selecao_mandante == instance.jogador.selecao:
                for evento in instance.jogo.eventos.filter(tipo='GOL'):
                    evento.jogo.gols_mandante += 1
            else:
                for evento in instance.jogo.eventos.filter(tipo='GOL'):
                    evento.jogo.gols_visitante += 1                              
        instance.jogo.save()
        return instance


class JogoSerializer(serializers.ModelSerializer):
    mandante_nome = serializers.CharField(source='selecao_mandante.nome', read_only=True)
    visitante_nome = serializers.CharField(source='selecao_visitante.nome', read_only=True)
    fase_display = serializers.CharField(source='get_fase_display', read_only=True)
    eventos = EventoJogoSerializer(many=True)
    resultado = serializers.SerializerMethodField()

    class Meta:
        model = Jogo
        fields = '__all__'

    def create(self, validated_data):
        eventos_data = validated_data.pop('eventos', [])
        jogo = Jogo.objects.create(**validated_data)
        for evento_data in eventos_data:
            evento_data.pop('jogo', None)
            EventoJogo.objects.create(jogo=jogo, **evento_data)
        return jogo

    def update(self, instance, validated_data):
        eventos_data = validated_data.pop('eventos', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if eventos_data is not None:
            instance.eventos.all().delete()
            for evento_data in eventos_data:
                evento_data.pop('jogo', None)
                EventoJogo.objects.create(jogo=instance, **evento_data)

        if instance.eventos.filter(tipo='GOL').exists():
            if instance.selecao_mandante == instance.jogador.selecao:
                instance.gols_mandante += 1
            else:
                instance.gols_visitante += 1              

        return instance

    def get_resultado(self, obj):
        if obj.status in ('AGENDADO', 'EM_ANDAMENTO', 'CANCELADO'):
            return None
        if obj.gols_mandante > obj.gols_visitante:
            return 'Mandante venceu'
        elif obj.gols_visitante > obj.gols_mandante:
            return 'Visitante venceu'
        return 'Empate'