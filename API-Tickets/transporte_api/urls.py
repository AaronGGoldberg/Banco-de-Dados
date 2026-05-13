from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from bilhetagem.views import (
    MunicipioViewSet,
    EmpresaTransporteViewSet,
    UsuarioViewSet,
    TipoTicketViewSet,
    TicketViewSet,
    TransporteViewSet,
    ValidadorViewSet,
    ValidacaoViewSet
)

from rest_framework import permissions

from drf_yasg.views import get_schema_view

from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Transporte",
        default_version='v1',
        description="Sistema de Tickets de Transporte Público",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()

router.register(r'municipios', MunicipioViewSet)
router.register(r'empresas', EmpresaTransporteViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'tipos-ticket', TipoTicketViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'transportes', TransporteViewSet)
router.register(r'validadores', ValidadorViewSet)
router.register(r'validacoes', ValidacaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(router.urls)),

    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),

    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]