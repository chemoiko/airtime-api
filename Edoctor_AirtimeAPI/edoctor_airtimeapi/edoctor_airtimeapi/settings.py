"""
Django settings for edoctor_airtimeapi project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MAX_RETRIES = 50
# 'mlsn.3cff4ba58d0de3cd05fee4c5ff5e57deae9798536ed5f93a39a976fe9d3aef7d'
# os.export
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

print("ENVIRONMENT:", os.environ.get('ENVIRONMENT'))
# SECURITY WARNING: keep the secret key used in production secret!
LOGIN_URL = "/dashboard"
SECRET_KEY = 'django-insecure-jcd=l-i5lni)3kx@y9_d!!3htn-khk#bu)&t2l=^#1ao9n*zdp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # ['127.0.0.1','127.0.0.1:8000','http://127.0.0.1','*']
TEMPLATES_ROOT = os.path.join(BASE_DIR, 'templates')
CORS_ALLOW_ALL_ORIGINS = True

# added django mail server:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailersend.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# os.environ.get('EMAIL_ID')
EMAIL_HOST_USER = 'MS_AW59iW@trial-k68zxl21p834j905.mlsender.net'
EMAIL_HOST_PASSWORD = 'CubCT9bpJnUpDCVb'  # os.environ.get('EMAIL_PW')

DEFAULT_FROM_EMAIL = 'noreply<no_reply@trial-k68zxl21p834j905.mlsender.net>'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'oauth2_provider',
    'airtimeapi',
    'apidashboard',
    "verify_email.apps.VerifyEmailConfig",
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
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]

ROOT_URLCONF = 'edoctor_airtimeapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'edoctor_airtimeapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    },

#    'dashboard_users': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db_db.sqlite3',
#    }
# }

DATABASE_ROUTERS = [
    "router.DashboardRouter"
]


ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'USER': 'default',
            'HOST': "ep-silent-moon-a4pyl2gv-pooler.us-east-1.aws.neon.tech",
            'PASSWORD': "tZvP2W5wAJsU",
            'NAME': "verceldb",
            'PORT': '5432'
        }
    }
else:
    raise ValueError(
        "Invalid ENVIRONMENT variable. Must be 'development' or 'production'.")

    # Password validation
    # https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_URL = 'templates/'
STATIC_URL = 'static/'
STATICFILES_DIRS = [

    BASE_DIR / "static",

]
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 'airtimeapi.airtime_auth.AirtimeAuthentication'
    ],
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
print(f"static root directory: {STATICFILES_DIRS}\n")
MEDIA_URLS = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
print(f"media root directory: {MEDIA_ROOT}\n")