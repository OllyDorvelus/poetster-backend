"""
Django settings for poetster project.
Generated by 'django-admin startproject' using Django 2.2.
Using django-configurations for settings
"""

import os
from datetime import timedelta

from configurations import Configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Base(Configuration):
    """
    Base settings for django project, common between dev, production, and any other environment
    """

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'ss^%$-fake-secret-key')

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'rest_framework',
        'rest_framework.authtoken',

        'django_extensions',
        'django_filters',
        'storages', # django-storages

        'user',
        'poem',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    # APPNAME.URLS
    ROOT_URLCONF = 'poetster.urls'

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

    # APPNAME.WSGI.APPLICATION
    WSGI_APPLICATION = 'poetster.wsgi.application'

    # Password validation
    # https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

    # REST FRAMEWORK CONFIGURATION

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        #    'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
    }

    # Internationalization
    # https://docs.djangoproject.com/en/2.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'America/New_York'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.2/howto/static-files/
   # STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
   # STATIC_URL = '/static/'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/vol/web/media'

    AUTH_USER_MODEL = 'user.User'


class Dev(Base):
    DEBUG = True

    ALLOWED_HOSTS = [
        '*',
        'localhost',
        '127.0.0.1:8000',
    ]

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(days=60),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    }


    CORS_ORIGIN_ALLOW_ALL = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('P_RDS_DB_NAME', ''),
            'USER': os.getenv('P_RDS_USERNAME', ''),
            'PASSWORD': os.getenv('P_RDS_PASSWORD', ''),
            'HOST': os.getenv('P_RDS_HOSTNAME', ''),
            'PORT': os.getenv('P_RDS_PORT', ''),
        }
    }

    # AWS SETTINGS
    AWS_LOCATION = 'static'
    AWS_ACCESS_KEY_ID =  os.getenv('OL_AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('OL_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('P_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    DEFAULT_FILE_STORAGE = 'poetster.storage_backends.MediaStorage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

    STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    AWS_DEFAULT_ACL = None


class Prod(Base):
    DEBUG = False

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('RDS_DB_NAME', ''),
            'USER': os.getenv('RDS_USERNAME', ''),
            'PASSWORD': os.getenv('RDS_PASSWORD', ''),
            'HOST': os.getenv('RDS_HOSTNAME', ''),
            'PORT': os.getenv('RDS_PORT', ''),
        }
    }

    # AWS SETTINGS
    AWS_LOCATION = 'static'
    AWS_ACCESS_KEY_ID =  os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    DEFAULT_FILE_STORAGE = 'poetster.storage_backends.MediaStorage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

    STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    AWS_DEFAULT_ACL = None
