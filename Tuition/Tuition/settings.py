
from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR/'Templates'

# In dev, load .env file; in prod, read from OS environment
if os.environ.get('ENVIRONMENT_NAME') != 'prod':
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')



ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'usermanager.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'rest_framework',
    'Home',
    'usermanager',
    'Tuitionmanager',
    'Teacher',
    'payment'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Tuition.urls'
CORS_ORIGIN_ALLOW_ALL = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMP_DIR],
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

WSGI_APPLICATION = 'Tuition.wsgi.application'


#Custom database configuration

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',  
#        'NAME': env('DB_NAME'),  
#        'USER': env('DB_USER'),  
#        'PASSWORD': env('DB_PASSWORD'),  
#        'HOST': env('DB_HOST'),  
#        'PORT': env('DB_PORT'),  
#        'OPTIONS': {  
#            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
#        }
#    }
#}


#PostgreSQL Supabase database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_DIR = BASE_DIR / 'static'
STATIC_URL = '/mystatic/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS =[
    STATIC_DIR,
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# DEBUG = int(env('DEBUG'))

# ''' sending email '''
# EMAIL_BACKEND = env('EMAIL_BACKEND')
# EMAIL_HOST =env('EMAIL_HOST')
# EMAIL_PORT =int(env('EMAIL_PORT'))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER =env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD =env('EMAIL_HOST_PASSWORD')
    
    
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')
ENVIRONMENT_NAME = os.environ.get('ENVIRONMENT_NAME', 'dev')
URL = os.environ.get('URL', 'http://localhost:8000')



EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# 2factor api secret key 
API_KEY = os.environ.get('API_KEY', '')

#razorpay credential
RAZOR_KEY_ID = os.environ.get('RAZOR_KEY_ID', '')
RAZOR_KEY_SECRET = os.environ.get('RAZOR_KEY_SECRET', '')



# Azure Storage account configuration
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME', '')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY', '')
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', '')
AZURE_OVERWRITE_FILES = os.environ.get('AZURE_OVERWRITE_FILES', 'False').lower() in ('true', '1', 'yes')


INSERT_DATA = os.environ.get('INSERT_DATA', 'False').lower() in ('true', '1', 'yes')