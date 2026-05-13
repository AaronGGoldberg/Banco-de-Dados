"""
Django settings for amazon project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-...'

DEBUG = True

# Permite acesso de qualquer host (ideal para desenvolvimento)
ALLOWED_HOSTS = ['*']


# ============================
# 🔥 CONFIGURAÇÃO PARA CODESPACES
# ============================

# Detecta se está rodando no GitHub Codespaces
codespace_name = os.getenv("CODESPACE_NAME")
codespace_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")

# 👉 MUITO IMPORTANTE:
# Permite que o Django entenda corretamente requisições vindas de proxy (Codespaces usa proxy HTTPS)
USE_X_FORWARDED_HOST = True

# 👉 Diz ao Django que o protocolo original era HTTPS (mesmo passando por proxy)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ============================
# 🔐 CSRF TRUSTED ORIGINS
# ============================

# Origens confiáveis (evita bloqueio do navegador)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "https://localhost:8000",
]

# Se estiver no Codespaces, adiciona automaticamente a URL pública
if codespace_name and codespace_domain:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{codespace_name}-8000.{codespace_domain}"
    )


# ============================
# 📦 APPS
# ============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🔥 Terceiros
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',          # Swagger
    'django_filters',
    'corsheaders',       # CORS

    # 📁 Seu app
    'backend',
]

# Libera requisições de qualquer origem (dev)
CORS_ALLOW_ALL_ORIGINS = True


# ============================
# ⚙️ DRF
# ============================

REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


# ============================
# 🔄 MIDDLEWARE
# ============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # 👉 PRECISA vir antes do CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'amazon.urls'


# ============================
# 🖥️ TEMPLATES
# ============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'amazon.wsgi.application'


# ============================
# 🗄️ BANCO DE DADOS (POSTGRES)
# ============================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'amazon',
        'USER': 'codespace',
        'PASSWORD': 'codespace',  # senha definida
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# ============================
# 🔐 VALIDAÇÃO DE SENHA
# ============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================
# 📄 SWAGGER
# ============================

SWAGGER_SETTINGS = {
    # 👉 Desativa autenticação por sessão no Swagger (evita conflito CSRF)
    'USE_SESSION_AUTH': False,

    # 👉 Permite acesso público ao Swagger (sem exigir login)
    'SECURITY_REQUIREMENTS': [],

    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization. Use: Bearer <token>'
        }
    }
}


# ============================
# 🌍 INTERNACIONALIZAÇÃO
# ============================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# ============================
# 📁 STATIC
# ============================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ============================
# 🔑 PK PADRÃO
# ============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'