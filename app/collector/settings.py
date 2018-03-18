from __future__ import absolute_import
"""
Django settings for collector project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from celery.schedules import crontab
from distutils.util import strtobool


def string_to_bool(string):
    return bool(strtobool(str(string)))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c&1d9t^p_ssul^n=i9t+xr5bd&l2yx*q&v1i@rv!x9_j2zp&_l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

DEV_MODE = string_to_bool(os.getenv('DEV_MODE', False))
RESIN = os.getenv('RESIN_DEVICE_UUID', False)


ALLOWED_HOSTS = []

if os.getenv('ALLOWED_HOSTS', False):
    ALLOWED_HOSTS += [os.getenv('ALLOWED_HOSTS')]

if DEV_MODE:
    ALLOWED_HOSTS += ['*']

ALLOWED_HOSTS += ['.resindevice.io']


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'chartit',
    'analytics.apps.AnalyticsConfig',
    'ble.apps.BleConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'collector.urls'

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
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'collector.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if not DEV_MODE:
    DATABASE_PATH = '/data/collector'
else:
    DATABASE_PATH = BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_PATH, 'db.sqlite3'),
    }
}

DEVICE_IGNORE_THRESHOLD = int(os.getenv('DEVICE_IGNORE_THRESHOLD', 5000))


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEV_MODE = os.getenv('DEV_MODE', False)

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_IMPORTS = ['ble.tasks', 'analytics.tasks']
CELERY_BEAT_SCHEDULE = {
    'ble-scan': {
        'task': 'ble.tasks.scan',
        'schedule': 60.0,
    },
    'generate-hourly-report': {
        'task': 'analytics.tasks.ble_generate_hourly_report',
        'schedule': crontab(minute=10),
    },
    'generate-hourly-report-backlog': {
        'task': 'analytics.tasks.ble_fill_report_backlog',
        'schedule': crontab(minute='*/10'),
        'args': ('H',)
    },
    'generate-daily-report': {
        'task': 'analytics.tasks.ble_generate_daily_report',
        'schedule': crontab(minute=5, hour=0),
    },
    'generate-daily-report-backlog': {
        'task': 'analytics.tasks.ble_fill_report_backlog',
        'schedule': crontab(minute='15'),
        'args': ('D',)
    },
    'generate-monthly-report': {
        'task': 'analytics.tasks.ble_generate_monthly_report',
        'schedule': crontab(minute=1, hour=3, day_of_month=1),
    },
    'generate-monthly-report-backlog': {
        'task': 'analytics.tasks.ble_fill_report_backlog',
        'schedule': crontab(minute='10'),
        'args': ('M',)
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
