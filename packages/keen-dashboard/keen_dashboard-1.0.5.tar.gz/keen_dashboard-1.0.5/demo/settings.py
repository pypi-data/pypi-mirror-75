import os
import sys

from environ import Env

env = Env(DEBUG=(bool, False))
env.read_env()

###############################
# PRINCIPAL                   #
###############################

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'r0k9of*6n#5ux92%)p2d8eevdg_tir)0d7@6!cyf2dwck-ng4p'
WSGI_APPLICATION = 'demo.wsgi.application'

DEBUG = env('DEBUG', False)
MEDIA_URL = env('MEDIA_URL')
STATIC_URL = env('STATIC_URL')

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
X_FRAME_OPTIONS = 'SAMEORIGIN'
CACHES = {
    'default': {
        'BACKEND': env('CACHE_BACKEND'),
        'LOCATION': env('CACHE_LOCATION'),
    }
}
SITE_ID = 1
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django_extensions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'keen_dashboard',
    'django.contrib.admin',
    'demo',
]

###############################
# ROTAS                       #
###############################

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo.urls'

###############################
# TEMPLATES                   #
###############################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "demo", 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

###############################
# BANCO DE DADOS              #
###############################

if 'sqlite' in env('DATABASE_ENGINE') or 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': env('DATABASE_ENGINE'),
            'NAME': env('DATABASE_NAME'),
            'HOST': env('DATABASE_HOST'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'PORT': env('DATABASE_PORT'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
                'use_unicode': True,
            },
        },
    }

###############################
# AUTENTICAÇÃO ############## #
###############################

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LOGIN_REDIRECT_URL = ''
LOGOUT_REDIRECT_URL = ''

###############################
# TIME AND LANGUAGE           #
###############################

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
AUTH_USER_MODEL = 'demo.Usuario'
USE_I18N = True
DATE_FORMAT = "d/m/Y"
DATE_INPUT_FORMATS = ('%d/%m/%Y',)
USE_L10N = True
USE_TZ = True

###############################
# GESTAO DE ARQUIVO ESTÁTICOS #
###############################

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

###############################
# EXTRA                       #
###############################

KEEN_CONFIG_CLASS = 'demo.config.AdminConfig'
