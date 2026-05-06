from django.db import models

# Create your models here.

class Grupo(models.Model):
    nome = models.CharField(max_length=1)
    descricao = models.TextField()
    
    def __str__(self):
        return f"Grupo {self.nome} - {self.descricao}"

class Tecnico(models.Model):
    nome = models.CharField(max_length=100)
    nacionalidade = models.CharField(max_length=100)
    nascimento = models.DateField()
    
    def __str__(self):
        return self.nome

class Selecao(models.Model):

    OPCOES_CONFEDERACAO = [
        ('CONMEBOL', 'CONMEBOL'),
        ('UEFA', 'UEFA'),
        ('CONCACAF', 'CONCACAF'),
        ('CAF', 'CAF'),
        ('AFC', 'AFC'),
        ('OFC', 'OFC'),
    ]

    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=3)
    confederacao = models.CharField(max_length=10, choices=OPCOES_CONFEDERACAO)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='selecoes')
    tecnico = models.OneToOneField(Tecnico, on_delete=models.SET_NULL, null=True, blank=True, related_name='selecao')
    escudo_url = models.URLField(blank=True, null=True)    
    def __str__(self):
        return f"{self.nome} - {self.grupo.nome}"

class Jogador(models.Model):

    OPCOES_POSICAO = [
        ('GOLEIRO', 'Goleiro'),
        ('ZAGUEIRO', 'Zagueiro'),        
        ('LATERAL', 'Lateral'),
        ('VOLANTE', 'Volante'),
        ('MEIO-CAMPISTA', 'Meio-campista'),
        ('ATACANTE', 'Atacante'),
    ]    

    nome = models.CharField(max_length=100)
    nome_guerra = models.CharField(max_length=100)
    selecao = models.ForeignKey(Selecao, on_delete=models.CASCADE, related_name='jogadores')
    posicao = models.CharField(max_length=20, choices=OPCOES_POSICAO)
    nascimento = models.DateField()
    numero_camisa = models.PositiveSmallIntegerField()
    suspenso = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nome} - {self.selecao.nome}"

class Jogo(models.Model):

    OPCOES_FASE = [
        ('fase de grupos', 'Fase de Grupos'),
        ('fase de 32', 'Fase de 32'),
        ('oitavas de final', 'Oitavas de Final'),
        ('quartas de final', 'Quartas de Final'),
        ('semifinal', 'Semifinal'),
        ('disputa de terceiro lugar', 'Disputa de Terceiro Lugar'),
        ('final', 'Final')
    ]

    STATUS = [
        ('AGENDADO', 'Agendado'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('ENCERRADO', 'Encerrado'),
        ('CANCELADO', 'Cancelado')
    ]

    selecao_mandante = models.ForeignKey(Selecao, on_delete=models.CASCADE, related_name='jogos_mandante')
    selecao_visitante = models.ForeignKey(Selecao, on_delete=models.CASCADE, related_name='jogos_visitante')
    fase = models.CharField(max_length=30, choices=OPCOES_FASE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='jogos', null=True, blank=True)
    data_hora = models.DateTimeField(auto_now_add=False)
    estadio = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    gols_mandante = models.PositiveSmallIntegerField(default=0)
    gols_visitante = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='AGENDADO')


    def __str__(self):
        return f"{self.selecao_mandante} x {self.selecao_visitante} - {self.fase}"

class EventoJogo(models.Model):
    
    TIPO = [
        ('GOL', 'Gol'),
        ('GOL_CONTRA', 'Gol Contra'),
        ('CARTAO_AMARELO', 'Cartão Amarelo'),
        ('CARTAO_VERMELHO', 'Cartão Vermelho'),
        ('SUBSTITUICAO', 'Substituição'),
    ]

    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name='eventos')
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='eventos')
    tipo = models.CharField(max_length=20, choices=TIPO)
    minuto = models.PositiveSmallIntegerField()
    acrescimo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo} - {self.minuto}' - {self.jogador.nome}"
