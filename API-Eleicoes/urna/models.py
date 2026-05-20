from django.db import models
from django.core.exceptions import ValidationError

# Modelo de Eleitor, representando um eleitor que pode votar nas eleições
class Eleitor(models.Model):

    nome = models.CharField(max_length=150)

    email = models.EmailField(unique=True)

    cpf = models.CharField(
        max_length=14,
        unique=True
    )

    data_nascimento = models.DateField()

    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

# Modelo de Eleição, representando uma eleição com seus detalhes e regras
class Eleicao(models.Model):

    TIPO_CHOICES = [
        ('estudantil', 'Estudantil'),
        ('sindical', 'Sindical'),
        ('associacao', 'Associacao'),
        ('condominio', 'Condominio'),
        ('conselho', 'Conselho'),
        ('outra', 'Outra'),
    ]

    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('aberta', 'Aberta'),
        ('encerrada', 'Encerrada'),
        ('apurada', 'Apurada'),
    ]

    titulo = models.CharField(max_length=200)

    descricao = models.TextField(blank=True)

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES
    )

    data_inicio = models.DateTimeField()

    data_fim = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='rascunho'
    )

    permite_branco = models.BooleanField(default=True)

    criada_por = models.ForeignKey(
        Eleitor,
        on_delete=models.PROTECT,
        related_name='eleicoes_criadas'
    )

    def clean(self):

        if self.data_fim <= self.data_inicio:
            raise ValidationError(
                'A data final precisa ser maior que a inicial'
            )

        if self.pk:

            eleicao_antiga = Eleicao.objects.get(pk=self.pk)

            fluxo = {
                'rascunho': ['aberta'],
                'aberta': ['encerrada'],
                'encerrada': ['apurada'],
                'apurada': []
            }

            status_antigo = eleicao_antiga.status
            status_novo = self.status

            if status_novo != status_antigo:

                if status_novo not in fluxo[status_antigo]:

                    raise ValidationError(
                        'Fluxo de status invalido'
                    )

    def __str__(self):
        return self.titulo

# Modelo de Candidato, representando um candidato que concorre em uma eleição
class Candidato(models.Model):

    eleicao = models.ForeignKey(
        Eleicao,
        on_delete=models.CASCADE,
        related_name='candidatos'
    )

    numero = models.PositiveIntegerField()

    nome = models.CharField(max_length=150)

    nome_urna = models.CharField(max_length=50)

    partido_ou_chapa = models.CharField(
        max_length=100,
        blank=True
    )

    proposta = models.TextField(blank=True)

    foto_url = models.URLField(blank=True)

    class Meta:

        unique_together = [
            ('eleicao', 'numero')
        ]

    def __str__(self):
        return f'{self.nome_urna} - {self.numero}'

# Modelo de Aptidão do Eleitor, representando a aptidão de um eleitor para votar em uma eleição específica
class AptidaoEleitor(models.Model):

    eleitor = models.ForeignKey(
        Eleitor,
        on_delete=models.PROTECT,
        related_name='aptidoes'
    )

    eleicao = models.ForeignKey(
        Eleicao,
        on_delete=models.CASCADE,
        related_name='aptos'
    )

    data_inclusao = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = [
            ('eleitor', 'eleicao')
        ]

    def __str__(self):
        return f'{self.eleitor.nome} - {self.eleicao.titulo}'

# Modelo de Registro de Votação, representando o registro de um eleitor que votou em uma eleição específica
class RegistroVotacao(models.Model):

    eleitor = models.ForeignKey(
        Eleitor,
        on_delete=models.PROTECT,
        related_name='registros_votacao'
    )

    eleicao = models.ForeignKey(
        Eleicao,
        on_delete=models.PROTECT,
        related_name='registros_votacao'
    )

    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = [
            ('eleitor', 'eleicao')
        ]

    def __str__(self):
        return f'{self.eleitor.nome} votou'

# Modelo de Voto, representando um voto registrado em uma eleição, podendo ser em branco ou para um candidato específico
class Voto(models.Model):

    eleicao = models.ForeignKey(
        Eleicao,
        on_delete=models.PROTECT,
        related_name='votos'
    )

    candidato = models.ForeignKey(
        Candidato,
        on_delete=models.PROTECT,
        related_name='votos',
        null=True,
        blank=True
    )

    em_branco = models.BooleanField(default=False)

    data_hora = models.DateTimeField(auto_now_add=True)

    comprovante_hash = models.CharField(
        max_length=64,
        unique=True
    )

    def clean(self):

        if self.em_branco and self.candidato is not None:

            raise ValidationError(
                'Voto em branco nao pode ter candidato'
            )

        if not self.em_branco and self.candidato is None:

            raise ValidationError(
                'Voto normal precisa ter candidato'
            )

    def __str__(self):

        if self.em_branco:
            return 'Voto em branco'

        return f'Voto em {self.candidato.nome_urna}'