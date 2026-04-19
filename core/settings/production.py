from os import getenv, path

from dotenv import load_dotenv

from .base import *

local_env_file = path.join(BASE_DIR, ".envs", ".env.prod")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


DEBUG = False
ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DB_NAME'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASSWORD'),
        'HOST': getenv('DB_HOST', 'localhost'),
        'PORT': getenv('DB_PORT', '5432'),
    }
}

CELERY_BROKER_URL = getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = getenv(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = TrueSESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = TrueSESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = TrueSESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
