from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'avaliacoes', views.AvaliacaoViewSet)
router.register(r'core-sets', views.CoreSetViewSet)
router.register(r'fontes-informacao', views.FonteInformacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('avaliar/', views.criar_avaliacao),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]