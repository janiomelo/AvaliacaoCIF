from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'avaliacoes', views.AvaliacaoViewSet)
router.register(r'pacientes', views.PacienteViewSet)
router.register(r'core-sets', views.CoreSetViewSet)
router.register(r'fontes-informacao', views.FonteInformacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('avaliar/', views.criar_avaliacao),
    path('usuario/', views.usuario),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]