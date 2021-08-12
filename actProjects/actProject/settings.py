from pathlib import Path
from . import my_settings
import os

# get envs from os
ENVS = {
    'ENV': os.getenv('ENV', 'DEV'),
    'SECRET_KEY': os.getenv('SECRET_KEY', ''),
    'DB_HOST': os.getenv('DB_HOST', ''),
    'DB_NAME': os.getenv('DB_NAME', ''),
    'DB_USER': os.getenv('DB_USER', ''),
    'DB_PASSWD': os.getenv('DB_PASSWD', ''),
    'DB_PORT': os.getenv('DB_PORT', ''),
}

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = ''
if ENVS['ENV'] == 'PROD':
    SECRET_KEY = ENVS['SECRET_KEY']
else:
    SECRET_KEY = my_settings.SECRET_KEY

# SECRET_KEY = os.environ.get('SECRET_KEY', my_settings.SECRET_KEY)
DEBUG = (os.environ.get('DEBUG', 'True') != 'False')

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# cdAWS_STORAGE_BUCKET_NAME = 'raonair-django'
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_REGION_NAME = 'ap-northeast-2'
# AWS_S3_CUSTOM_DOMAIN = 'd36nnc6k71ix1t.cloudfront.net'


ALLOWED_HOSTS = ['*']

# Application definition

#######################################
# 개발용, cache를 dummy cache로 설정, dummy cache는 아무것도 하지 않는다
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
#######################################

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App.apps.AppConfig',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'actProject.urls'

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

WSGI_APPLICATION = 'actProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {}
if ENVS['ENV'] == 'PROD':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': ENVS['DB_HOST'],
            'NAME': ENVS['DB_NAME'],
            'USER': ENVS['DB_USER'],
            'PASSWORD': ENVS['DB_PASSWD'],
            'PORT': ENVS['DB_PORT'],
        }
    }
else:
    DATABASES = my_settings.DATABASES

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# CORS setting
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000', 'https://localhost:3000',
    'http://raonair.art', 'https://raonair.art',
    'http://raonair.netlify.app', 'https://raonair.netlify.app', ]
CORS_ALLOW_CREDENTIALS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'raonairjs@gmail.com' # ex) bum752@gmail.com
EMAIL_HOST_PASSWORD = my_settings.EMAIL_HOST_PASSWORD # ex) P@ssw0rd
SERVER_EMAIL = 'raonairjs@gmail.com' # ex) bum752@gmail.com
DEFAULT_FROM_MAIL = 'raonair_js' # ex) bum752