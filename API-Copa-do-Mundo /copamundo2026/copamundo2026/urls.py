from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from torneio.views import (
    GrupoViewSet, TecnicoViewSet, SelecaoViewSet,
    JogadorViewSet, JogoViewSet, EventoJogoViewSet,
)


schema_view = get_schema_view(
    openapi.Info(
        title='Copa do Mundo 2026 API',
        default_version='v1',
    ),
    public=True,
)

router = DefaultRouter()
router.register(r'grupos', GrupoViewSet)
router.register(r'tecnicos', TecnicoViewSet)
router.register(r'selecoes', SelecaoViewSet)
router.register(r'jogadores', JogadorViewSet)
router.register(r'jogos', JogoViewSet)
router.register(r'eventos-jogo', EventoJogoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
