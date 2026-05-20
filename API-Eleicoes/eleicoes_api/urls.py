"""
URL configuration for eleicoes_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from urna.views import (

    EleitorViewSet,
    EleicaoViewSet,
    CandidatoViewSet,
    AptidaoEleitorViewSet,
    RegistroVotacaoViewSet,
    VotoViewSet,
    verificar_comprovante,
    gerar_qrcode
)

router = DefaultRouter()

router.register(
    'eleitores',
    EleitorViewSet
)
router.register(
    'eleicoes',
    EleicaoViewSet
)
router.register(
    'candidatos',
    CandidatoViewSet
)
router.register(
    'aptidoes',
    AptidaoEleitorViewSet
)
router.register(
    'registros-votacao',
    RegistroVotacaoViewSet
)
router.register(
    'votos',
    VotoViewSet
)

schema_view = get_schema_view(

    openapi.Info(
        title="API Eleicoes",
        default_version='v1',
        description="Sistema de Eleicoes"
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny
    ],
)


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'eleicoes_api/',
        include(router.urls)
    ),
    path(
        'eleicoes_api/verificar-comprovante/',
        verificar_comprovante,
        name='verificar-comprovante'
    ),
    path(
        'eleicoes_api/comprovantes/qr/',
        gerar_qrcode
    ),
    path(
        'swagger/',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0
        ),
        name='swagger'
    ),
    path(
        'redoc/',
        schema_view.with_ui(
            'redoc',
            cache_timeout=0
        ),
        name='redoc'
    ),
]
