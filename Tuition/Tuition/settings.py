
from pathlib import Path
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent
import environ
env = environ.Env()
environ.Env.read_env(BASE_DIR/ '.env')
TEMP_DIR = BASE_DIR/'Templates'



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


#Default database confguration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
    
    
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ENVIRONMENT_NAME = env('ENVIRONMENT_NAME')
URL = env('URL')
DEBUG = eval(env('DEBUG'))



EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST =env('EMAIL_HOST')
EMAIL_PORT =int(env('EMAIL_PORT'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER =env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD =env('EMAIL_HOST_PASSWORD')

# 2factor api secret key 
API_KEY =env('API_KEY')

#razorpay credential
RAZOR_KEY_ID = env('RAZOR_KEY_ID')
RAZOR_KEY_SECRET = env('RAZOR_KEY_SECRET')
print(DEBUG)


# Azure Storage account configuration
DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE')
AZURE_ACCOUNT_NAME = env('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = env('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = env('AZURE_CONTAINER')
AZURE_OVERWRITE_FILES = eval(env('AZURE_OVERWRITE_FILES'))


