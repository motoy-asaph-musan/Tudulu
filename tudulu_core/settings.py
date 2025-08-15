from django.urls import reverse_lazy

from pathlib import Path

import os
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3q29h-oa0xw4e9$i4gy9pnedefuel#c7tqb*o*8_lkt@!8&#1g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['*']

# ALLOWED_HOSTS = ['tudulu.onrender.com']

# ALLOWED_HOSTS = ['tudulu.onrender.com', 'localhost', '127.0.0.1']

# settings.py
SERVICE_ALERT_RECIPIENTS = [
    "maintenance@example.com",
    "supervisor@example.com",
    "admin@example.com",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'equipment',
    'equipment.apps.EquipmentConfig',
    # 'users',
    'users.apps.UsersConfig',
    'clearcache',
    'widget_tweaks',
    'django_crontab',
]


# CRONJOBS = [
#     ('0 8 * * *', 'equipment.tasks.send_service_alerts'),  # Every day at 8 AM
# ]
CRONJOBS = [
    ('0 9 * * *', 'django.core.management.call_command', ['send_due_equipment_emails']),
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

ROOT_URLCONF = 'tudulu_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # 👈 add this
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


WSGI_APPLICATION = 'tudulu_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'users.CustomUser'

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# For development, you can add this:
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# For production, collectstatic copies files here:
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN_URL = 'login'  # Points to your login URL name
# LOGIN_REDIRECT_URL = 'home'  # Where to redirect after login
# LOGOUT_REDIRECT_URL = 'login'

LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = '/equipment/home/'  # after login, go to home
LOGIN_REDIRECT_URL = 'equipment:equipment_list' #feed/home page

LOGOUT_REDIRECT_URL = '/'  # after logout, come back to login
ACCOUNT_LOGOUT_ON_GET = False #default

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'admin@tudulu.com'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'motoyasaphmusan@gmail.com'
# EMAIL_HOST_PASSWORD = 'Tudulu@Uganda36!'

#For sending emails; whereas for Gmail, we shall need the password
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your_email@example.com"
EMAIL_HOST_PASSWORD = "your_password_or_app_password"

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_TIMEZONE = 'Africa/Kampala'
CELERY_ENABLE_UTC = False

# Stripe for payment
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# In .env (and load with python-decouple or similar):

# STRIPE_PUBLIC_KEY=pk_test_xxx
# STRIPE_SECRET_KEY=sk_test_xxx