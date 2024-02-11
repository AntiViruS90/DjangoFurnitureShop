"""
Django settings for DjangoFurnitureShop project.

Generated by 'django-admin startproject' using Django 4.2.7

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd+3hh($sfwvkzy4dn)9=s5g9mdi6zq9wh!$a!cxxw%4c4!@jpy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# DEBUG = False     # Server
# ALLOWED_HOSTS = ['SlavaNikitin.pythonanywhere.com',]      # Server

STATICFILES_DIRS = [(os.path.join(BASE_DIR, "static"))]

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
# )

MEDIA_ROOT = 'media/'
MEDIA_URL = 'media/'

# Application definition

INSTALLED_APPS = [
    'index.apps.IndexConfig',
    'register.apps.RegisterConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "crispy_forms",
    "crispy_bootstrap4",
    'multiupload',

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

ROOT_URLCONF = 'DjangoFurnitureShop.urls'

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

WSGI_APPLICATION = 'DjangoFurnitureShop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2.7/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2.7/howto/static-files/

STATIC_URL = '/static/'
# MEDIA_URL = '/media/'     # Server
# STATIC_ROOT = '/home/SlavaNikitin/ServerFurnitureShop/static'     # Server
# MEDIA_ROOT = '/home/SlavaNikitin/ServerFurnitureShop/media'       # Server

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

################# Mail.ru ###################

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST = 'smtp.mail.ru'
# EMAIL_HOST_USER = 'slava-nikitin-1990@mail.ru'
# EMAIL_HOST_PASSWORD = 'XfrCRSqDrC2VfgpyiZUc'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# EMAIL_SERVER = EMAIL_HOST_USER
# EMAIL_ADMIN = EMAIL_HOST_USER
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

################# Yandex.ru ###################
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_PORT = 587    # EMAIL_USE_SSL = True  EMAIL_PORT = 465
# EMAIL_USE_TLS = True

# EMAIL_HOST_USER = 'AntiViruS2290@yandex.ru'
# EMAIL_HOST_PASSWORD = 'cznapkcwkpqvqtyx'

# EMAIL_SERVER = EMAIL_HOST_USER
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_ADMIN = EMAIL_HOST_USER

################# Gmail.com ###################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "slava90nikitin90@gmail.com"
EMAIL_HOST_PASSWORD = 'qzyd pnia lqbz xdtv'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_SERVER = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER
