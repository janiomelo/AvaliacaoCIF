from django.contrib import admin
from . import models


admin.site.register(models.CoreSet)
admin.site.register(models.Categoria)
admin.site.register(models.FonteInformacao)
admin.site.register(models.Classificacao)
admin.site.register(models.Qualificador)
admin.site.register(models.Pergunta)
admin.site.register(models.Pessoa)
admin.site.register(models.Avalicao)
admin.site.register(models.Resposta)
admin.site.register(models.RespostaQualificador)
