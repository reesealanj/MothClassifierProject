"""
Django settings for moth_api project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

from constants import REDIS_HOST, REDIS_PORT
from conf.api_keys import FCM_KEY
from conf.secrets import (
    DJANGO_DATABASE,
    DJANGO_SECRET_KEY,
    EMAIL_USER,
    EMAIL_PASSWORD,
    REDIS_PASS,
    SERVER_IP,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [SERVER_IP]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'crispy_forms',
    'django_fsm',
    'drf_yasg',
    'drf_firebase_auth',
    'fcm_django',
    'api.apps.ApiConfig',
    'users.apps.UsersConfig',
    'images.apps.ImagesConfig',
    'jobs.apps.JobsConfig',
    'classifications.apps.ClassificationsConfig',
    'ml_models.apps.MLModelsConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomFirebaseAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'moth_api.drf_defaults.StandardResultsSetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'moth_api.urls'

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

WSGI_APPLICATION = 'moth_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = DJANGO_DATABASE


# Authentication settings
AUTH_USER_MODEL = 'users.User'
DRF_FIREBASE_AUTH = {
    'FIREBASE_SERVICE_ACCOUNT_KEY': 'conf/firebase.json',
    'FIREBASE_AUTH_HEADER_PREFIX': 'Bearer',
    'ALLOW_ANONYMOUS_REQUESTS': True,
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {'BearerAuth': {'type': 'http', 'scheme': 'bearer',}}
}


REDOC_SETTINGS = {
    'PATH_IN_MIDDLE': True,
}


# Celery settings
BROKER_URL = f'redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Firebase Cloud Messaging (FCM) settings
FCM_DJANGO_SETTINGS = {'FCM_SERVER_KEY': FCM_KEY}


# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = EMAIL_USER
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
EMAIL_PORT = 587


# Admins and Managers Settings
ADMINS = [('MothClassifier', EMAIL_USER)]
