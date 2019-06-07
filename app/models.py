from django.db import models
from django.contrib.auth.models import User


class FonteInformacao(models.Model):
    descricao = models.CharField(max_length=60)

    def __str__(self):
        return self.descricao


class CoreSet(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Classificacao(models.Model):
    nivel = models.IntegerField()
    prefixo = models.CharField(max_length=2, null=True, blank=True)
    descricao = models.CharField(max_length=60)

    def __str__(self):
        return "{0} - {1}".format(self.nivel, self.descricao)

    class Meta:
        ordering = ['nivel']


class Qualificador(models.Model):
    descricao = models.CharField(max_length=60)

    def __str__(self):
        return self.descricao


class Categoria(models.Model):
    coreSet = models.ForeignKey(
        CoreSet, on_delete=models.CASCADE, related_name='categorias')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    classificacoes = models.ManyToManyField(Classificacao)
    qualificadores = models.ManyToManyField(Qualificador)

    def __str__(self):
        return self.titulo


class Pergunta(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name='perguntas')
    codigo = models.CharField(max_length=4)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.codigo, self.titulo)


class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, unique=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    nascimento = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    endereco = models.CharField(max_length=100,null=True, blank=True)
    bairro = models.CharField(max_length=70, null=True, blank=True)
    cidade = models.CharField(max_length=70, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)
    terapeuta = models.ForeignKey(
        'Pessoa', null=True, blank=True, on_delete=models.CASCADE)
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome


class Avalicao(models.Model):
    coreSet = models.ForeignKey(
        CoreSet, on_delete=models.CASCADE, related_name='avaliacoes')
    terapeuta = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE, related_name="avaliacoes_terapeuta")
    paciente = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE, related_name="avaliacoes_paciente")
    data = models.DateTimeField(auto_now_add=True)


class Resposta(models.Model):
    avaliacao = models.ForeignKey(Avalicao, on_delete=models.CASCADE)
    fonteInformacao = models.ForeignKey(
        FonteInformacao, on_delete=models.DO_NOTHING)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.DO_NOTHING)
    descricaoProblema = models.TextField(null=True, blank=True)


class RespostaQualificador(models.Model):
    resposta = models.ForeignKey(
        Resposta, on_delete=models.CASCADE,
        related_name='respostas_qualificadores')
    classificacao = models.ForeignKey(
        Classificacao, on_delete=models.DO_NOTHING)
    qualificador = models.ForeignKey(
        Qualificador, on_delete=models.DO_NOTHING)
