"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# for using .env
import environ
env = environ.Env()
# if it doesn't deploys at heroku it would read .env
HEROKU_ENV = env.bool('HEROKU_ENV', default=False)
if not HEROKU_ENV:
    env.read_env('.env')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
# SECRET_KEY = 'gcb6xd4s_hu^q!f-hnue4i1#5zrxp4pqsbwdu(^q$cb(y3!*-d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'firebase_auth',

    'v1.apps.V1Config',
    'person.apps.PersonConfig',
    'task.apps.TaskConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
if not HEROKU_ENV:
    DATABASES = {
        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # }
        'default': {
            'ENGINE':'django.db.backends.postgresql_psycopg2',
            'NAME':'dimbula',
            'USER':os.environ.get('DB_USER'),
            'PASSWORD':os.environ.get('DB_PASSWORD'),
            'HOST':'',
            'PORT':'',
        }
    }
else :
    # TODO : is it requirement?
    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES = {
        'default': dj_database_url.config()
    }
    
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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'firebase_auth.authentication.FirebaseAuthentication',
    ]
}


#if firebase secret information .json is not exist generate json file
file_name = 'firebase-info.json'
if not os.path.exists(os.path.join(BASE_DIR, file_name)):
    import json
    info = {
        "type": env('FIREBASE_TYPE'),
        "project_id": env('FIREBASE_PROJECT_ID'),
        "private_key_id": env('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": env('FIREBASE_PRIVATE_KEY').replace("\\n", "\n"),
        "client_email": env('FIREBASE_CLIENT_EMAIL'),
        "client_id": env('FIREBASE_CLIENT_ID'),
        "auth_uri": env('FIREBASE_AUTH_URI'),
        "token_uri": env('FIREBASE_TOKEN_URI'),
        "auth_provider_x509_cert_url": env('FIREBASE_AUTH_PROVIDER_X509_CERT_URI'),
        "client_x509_cert_url": env('FIREBASE_CLIENT_X509_CERT_URL')
    }
    with open(os.path.join(BASE_DIR, file_name), 'w') as outfile:
        json.dump(info, outfile)

# <==== Firebase Authentication settings
FIREBASE_AUTH = {
    # path to JSON file with firebase secrets
    'FIREBASE_SERVICE_ACCOUNT_KEY':
        os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY', os.path.join(BASE_DIR, file_name)),
    # allow creation of new local user in db
    'FIREBASE_CREATE_LOCAL_USER':
        os.getenv('FIREBASE_CREATE_LOCAL_USER', True),
    # commonly JWT or Bearer (e.g. JWT <token>)
    'FIREBASE_AUTH_HEADER_PREFIX':
        os.getenv('FIREBASE_AUTH_HEADER_PREFIX', 'Bearer'),
    # verify that JWT has not been revoked
    'FIREBASE_CHECK_JWT_REVOKED':
        os.getenv('FIREBASE_CHECK_JWT_REVOKED', True),
    # require that firebase user.email_verified is True
    'FIREBASE_AUTH_EMAIL_VERIFICATION':
        os.getenv('FIREBASE_AUTH_EMAIL_VERIFICATION', True),
}
# ====>

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    env('FRONTEND_URL'),
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://dimbula-\w+-niwa-niwa\.vercel\.app$",
]


# for Heroku
import django_heroku
django_heroku.settings(locals())
