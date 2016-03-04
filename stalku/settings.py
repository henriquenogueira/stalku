import os

from decouple import config, Csv
from dj_database_url import parse as dburl

########################################################################
# Basic configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

########################################################################
# Application definition

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'test_without_migrations',
]

LOCAL_APPS = [
    'stalku.core.apps.CoreConfig',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stalku.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stalku.wsgi.application'

########################################################################
# Database

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
}

########################################################################
# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

########################################################################
# Internationalization

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

########################################################################
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

########################################################################
# Specific DAC URLS

PUBLIC_MENU_URL = 'http://www.daconline.unicamp.br/altmatr/menupublico.do'
SEARCH_LECTURE_URL = 'http://www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do'

LECTURES_URLS = {
    'grad': {
        'institutes': 'http://www.dac.unicamp.br/sistemas/horarios/grad/G{}S0/indiceP.htm',
        'lectures': 'http://www.dac.unicamp.br/sistemas/horarios/grad/G{}S0/{}.htm',
        'lecture': 'http://www.dac.unicamp.br/sistemas/horarios/grad/G{}S0/{}.htm'
    },
    'pos': {
        'institutes': 'http://www.dac.unicamp.br/sistemas/horarios/pos/P{}S/indiceP.htm',
        'lectures': 'http://www.dac.unicamp.br/sistemas/horarios/pos/P{}S/{}.htm',
        'lecture': 'http://www.dac.unicamp.br/sistemas/horarios/pos/P{}S/{}.htm'
    }
}
