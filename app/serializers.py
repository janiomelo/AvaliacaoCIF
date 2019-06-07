from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth.models import User
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'email', 'last_name', 'is_staff']


class ClassificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classificacao
        fields = '__all__'


class QualificadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Qualificador
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    qualificadores = QualificadorSerializer(read_only=True, many=True)
    classificacoes = ClassificacaoSerializer(read_only=True, many=True)
    perguntas = serializers.SerializerMethodField()

    class Meta:
        model = models.Categoria
        fields = '__all__'

    def get_perguntas(self, obj):
        perguntas = models.Pergunta.objects.filter(categoria=obj.id)
        return PerguntaSerializer(perguntas, many=True).data


class CoreSetSerializer(serializers.ModelSerializer):
    categorias = serializers.SerializerMethodField()

    class Meta:
        model = models.CoreSet
        fields = '__all__'

    def get_categorias(self, obj):
        categorias = models.Categoria.objects.filter(coreSet = obj.id)
        return CategoriaSerializer(categorias, many=True).data


class FonteInformacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FonteInformacao
        fields = '__all__'


class PerguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pergunta
        fields = '__all__'


class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pessoa
        fields = ['id','nome','user','cpf','sexo', 'nascimento','endereco',
        'bairro','cidade','estado','cep','terapeuta', 'observacoes', 'email',
        'telefone']


class CategoriaRespostaSerializer(serializers.ModelSerializer):
    respostas = serializers.ListField(
        read_only=True, required=False, allow_empty=True, allow_null=True)

    class Meta:
        model = models.Categoria
        fields = '__all__'


class AvaliacaoSimplesSerializer(serializers.ModelSerializer):
    paciente = PessoaSerializer()
    terapeuta = PessoaSerializer()

    class Meta:
        model = models.Avalicao
        fields = '__all__'


class AvaliacaoSerializer(serializers.ModelSerializer):
    paciente = PessoaSerializer()
    terapeuta = PessoaSerializer()
    categorias = serializers.SerializerMethodField()

    class Meta:
        model = models.Avalicao
        fields = '__all__'

    def get_categorias(self, obj):
        categorias = models.Categoria.objects.filter(coreSet=obj.coreSet)
        for c in categorias:
            r = models.Resposta.objects.select_related('pergunta')
            r = r.filter(Q(avaliacao=obj.id) & Q(pergunta__categoria=c.id))
            c.respostas = RespostaSerializer(r, many=True).data
        return CategoriaRespostaSerializer(categorias, many=True).data


class RespostaSerializer(serializers.ModelSerializer):
    pergunta = PerguntaSerializer()
    qualificadores = serializers.SerializerMethodField()

    class Meta:
        model = models.Resposta
        fields = '__all__'

    def get_qualificadores(self, obj):
        qualificadores = models.RespostaQualificador.objects.filter(
            resposta=obj.id
        )
        return RespostaQualificadorSerializer(qualificadores, many=True).data


class RespostaQualificadorSerializer(serializers.ModelSerializer):
    classificacao = ClassificacaoSerializer()
    qualificador = QualificadorSerializer()

    class Meta:
        model = models.RespostaQualificador
        fields = '__all__'


