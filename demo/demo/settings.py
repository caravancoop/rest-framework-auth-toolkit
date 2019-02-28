"""Django settings for demo project."""

import os

from django.core.management.utils import get_random_secret_key

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

if os.getenv('RAT_TESTING'):
    os.environ['DEMO_SECRET_KEY'] = get_random_secret_key()
    os.environ['DEMO_FACEBOOK_APP_ID'] = 'fb app id'
    os.environ['DEMO_FACEBOOK_APP_SECRET_KEY'] = 'fb app key'


SECRET_KEY = os.getenv('DEMO_SECRET_KEY',
                       '1(9v73@)*ws6i(v_i5*_4ty^+ji0@7u($6onk7pt-_ncxkqs@@')

DEBUG = True

FACEBOOK_APP_ID = os.environ['DEMO_FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET_KEY = os.environ['DEMO_FACEBOOK_APP_SECRET_KEY']

DATABASES = {
    'default': dj_database_url.parse(os.environ['DATABASE_URL']),
}

SITE_ID = 1
ROOT_URLCONF = 'demo.urls'
WSGI_APPLICATION = 'wsgi.application'
AUTH_USER_MODEL = 'accounts.User'

# ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'debug_toolbar',
    'rest_auth_toolkit.app.RestAuthToolkitConfig',

    'demo.accounts.app.AccountsConfig',
    'demo.pages.app.PagesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.' + name}
    for name in ['UserAttributeSimilarityValidator', 'MinimumLengthValidator',
                 'CommonPasswordValidator', 'NumericPasswordValidator']
]


TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'

USE_TZ = True
TIME_ZONE = 'UTC'


STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # This is the real authn policy for API clients
        'demo.accounts.authentication.APITokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


REST_AUTH_TOOLKIT = {
    'email_confirmation_class': 'demo.accounts.models.EmailConfirmation',
    'email_confirmation_from': 'auth-demo@localhost',
    'email_confirmation_lookup_field': 'external_id',
    'api_token_class': 'demo.accounts.models.APIToken',
}
