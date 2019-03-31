from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (
    MethodNotAllowed, ValidationError, APIException)
from django.db import transaction
from . import models, serializers



class CoreSetViewSet(viewsets.ModelViewSet):
    queryset = models.CoreSet.objects.all()
    serializer_class = serializers.CoreSetSerializer


class FonteInformacaoViewSet(viewsets.ModelViewSet):
    queryset = models.FonteInformacao.objects.all()
    serializer_class = serializers.FonteInformacaoSerializer


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = models.Avalicao.objects.all()
    serializer_class = serializers.AvaliacaoSerializer


def tem_categoria_na_resposta(categoria_id, respostas):
    for resposta in respostas:
        if resposta['categoria'] == categoria_id:
            return True
    return False


def tem_pergunta_na_resposta(pergunta_id, respostas):
    for categoria in respostas:
        for resposta in categoria.get('respostas', []):
            if resposta['pergunta'] == pergunta_id:
                return True
    return False


def tem_qualificador_na_resposta(quali_id, respostas):
    return True


class BadRequest(APIException):
    def __init__(self, detail):
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(detail=detail, code=self.status_code)


def valida_avaliacao(avaliacao):
    try:
        coreSet = models.CoreSet.objects.get(pk=avaliacao.get('coreSet'))
    except models.CoreSet.DoesNotExist:
        raise ValidationError("Core Set é obrigatório.")

    respostas = avaliacao.get('respostas', [])

    if len(avaliacao.get('respostas')) == 0:
        raise BadRequest(detail="Responda todas as perguntas.")

    for categoria in coreSet.categorias.all():
        if not tem_categoria_na_resposta(categoria.id, respostas):
            raise ValidationError(
                "Categoria '{0}' não respondida.".format(
                    categoria.titulo)
            )
        for pergunta in categoria.perguntas.all():
            if not tem_pergunta_na_resposta(pergunta.id, respostas):
                raise ValidationError(
                    "Pergunta '{0}' não respondida.".format(
                        pergunta.titulo)
                )
        for quali in categoria.qualificadores.all():
            if not tem_qualificador_na_resposta(quali.id, respostas):
                raise ValidationError(
                    "Qualificador '{0}' da pergunta '{1}' não respondido.".format(
                        quali.descricao, pergunta.titulo)
                )

def gravar_avaliacao(avaliacao_dados):
    coreSet = models.CoreSet.objects.get(pk=avaliacao_dados.get('coreSet'))
    terapeuta = models.Pessoa.objects.get(pk=1)
    paciente = models.Pessoa.objects.get(pk=2)
    avaliacao = models.Avalicao.objects.create(
        paciente=paciente, terapeuta=terapeuta, coreSet=coreSet)

    for c in avaliacao_dados['respostas']:
        for r in c['respostas']:
            pergunta = models.Pergunta.objects.get(pk=r['pergunta'])
            if r['fonteInformacao'] is None:
                raise ValidationError(
                    "Preencha a fonte de informação da pergunta '{0}'".format(
                        pergunta.titulo
                    )
                )
            fonte = models.FonteInformacao.objects.get(pk=r['fonteInformacao'])

            resposta = models.Resposta.objects.create(
                avaliacao=avaliacao, fonteInformacao=fonte, pergunta=pergunta,
                descricaoProblema='')

            for q in r['qualificadores']:
                classificacao = models.Classificacao.objects.get(
                    pk=q['classificacao'])
                qualificador = models.Qualificador.objects.get(
                    pk=q['qualificador']
                )
                models.RespostaQualificador.objects.create(
                    resposta=resposta, classificacao=classificacao,
                    qualificador=qualificador
                )


@api_view(['POST'])
@transaction.atomic
def criar_avaliacao(request):
    '''
    {"respostas":
        [{"categoria":1,"respostas":
            [{"pergunta":1,"qualificadores":
                    [{"qualificador":3,"classificacao":"5"},
                    {"qualificador":2,"classificacao":"6"},
                    {"qualificador":1,"classificacao":"3"}],
            "fonteInformacao":null}]
        },{"categoria":2,"respostas":
            [{"pergunta":2,"qualificadores":[],"fonteInformacao":"4"}]
        },{"categoria":3,"respostas":
            [{"pergunta":3,"qualificadores":
                    [{"qualificador":6,"classificacao":"4"}],
            "fonteInformacao":null}]}]}}
    '''
    if request.method == 'POST':
        valida_avaliacao(request.data)
        gravar_avaliacao(request.data)
        return Response({"message": "OK!", "data": request.data})
    raise MethodNotAllowed
