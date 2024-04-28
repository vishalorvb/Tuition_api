
from pathlib import Path
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent
import environ
env = environ.Env()
environ.Env.read_env(BASE_DIR/ '.env')
TEMP_DIR = BASE_DIR/'Templates'



SECRET_KEY = "django-insecure-ct4r=zj1svv8=!#8y((jo8wd*ihgpwz9@x-4!%3l))j6w)=nb&"
# DEBUG = int(env('DEBUG'))
DEBUG = True
ENVIRONMENT_NAME = "dev"
URL = "http://127.0.0.1:8000/"

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'usermanager.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
SIMPLE_JWT = {
    #'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
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


# ''' sending email '''
# EMAIL_BACKEND = env('EMAIL_BACKEND')
# EMAIL_HOST =env('EMAIL_HOST')
# EMAIL_PORT =int(env('EMAIL_PORT'))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER =env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD =env('EMAIL_HOST_PASSWORD')

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST ="smtp.gmail.com"
EMAIL_PORT =587
EMAIL_USE_TLS = True
EMAIL_HOST_USER ="v.kumar70760@gmail.com"
EMAIL_HOST_PASSWORD ="Vb&third1"

# 2factor api secret key 
API_KEY ="5ddefe3a-b029-11ec-a4c2-0200cd936042"

#razorpay credential
RAZOR_KEY_ID ="rzp_test_QvSukHJCQx98aF"
RAZOR_KEY_SECRET ="C32zIZ9XCiHE0DYdGLC6lUI9"



# Azure Storage account configuration
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = 'profilephoto'
AZURE_ACCOUNT_KEY = 'ZkbP9qJXCdxw+HmuuMdOKP4PulVGOGicZVxNvb14/Hj2USB3s2Cydz8x4ZJ3uj6a/mSWS8yQ78cu+AStIXYb8A=='
AZURE_CONTAINER = 'profilepic'
AZURE_OVERWRITE_FILES = True


# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
# STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'