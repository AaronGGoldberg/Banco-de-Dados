from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.views import ClienteViewSet, VendedorViewSet, ProdutoViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# ============================
# 📄 CONFIGURAÇÃO DO SWAGGER
# ============================

# 👉 NÃO definimos url manualmente aqui
# O Django agora detecta automaticamente com base na requisição (graças ao proxy config no settings)

schema_view = get_schema_view(
    openapi.Info(
        title='Amazon API',
        default_version='v1',
        description='API RESTful para gerenciamento de pedidos',
        contact=openapi.Contact(email='contato@amazon.com'),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(),
)


# ============================
# 🔗 ROUTER DRF
# ============================

router = DefaultRouter()

# Endpoint:
# /amazon_api/clientes/
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'vendedores', VendedorViewSet, basename='vendedor')
router.register(r'produtos', ProdutoViewSet, basename='produto')


# ============================
# 🌐 URLS
# ============================

urlpatterns = [
    path('admin/', admin.site.urls),

    # API principal
    path('amazon_api/', include(router.urls)),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

    # Redoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),

    # 👉 JSON bruto (IMPORTANTE para debug)
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]