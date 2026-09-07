"""
Django settings for config project.
Configuración optimizada para Explora Pucusana (Local + Render Ready).
"""
import os
from pathlib import Path
from dotenv import load_dotenv # Importamos para leer el archivo .env

# Cargar variables de entorno
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')

# ## CAMBIO IMPORTANTE: Controlamos el modo Debug desde el archivo .env
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ## CAMBIO IMPORTANTE: Permitimos cualquier host para desarrollo y Render
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # ## TUS APPS
    'turismo', # Tu app principal
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # ## CAMBIO IMPORTANTE: WhiteNoise sirve los archivos estáticos en producción
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'DIRS': [], # Dejamos esto vacío porque usaremos las carpetas dentro de la app 'turismo'
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'turismo.context_processors.alerta_perfil',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Por ahora usamos SQLite. Cuando integremos Supabase, cambiaremos esto.
# DATABASES = {
  #  'default': {
   #     'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': BASE_DIR / 'db.sqlite3',
    #}
#}
# Asegúrate de importar y configurar os para leer el archivo .env si usas herramientas como python-dotenv
# Si no usas python-dotenv, puedes leerlas directamente usando os.environ.get si tu hosting las inyecta.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Password validation
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
# ## CAMBIO IMPORTANTE: Configuración regional para Perú

LANGUAGE_CODE = 'es-pe'  # Español de Perú

TIME_ZONE = 'America/Lima' # Hora de Perú

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# ## CAMBIO IMPORTANTE: Configuración para que Tailwind y CSS funcionen en Render

STATIC_URL = 'static/'

# Aquí es donde Django buscará archivos estáticos durante el desarrollo
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'turismo/static'), # Asegúrate de crear esta carpeta después
]

# Aquí es donde Django recolectará todos los archivos cuando hagas "deploy"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Motor de almacenamiento para producción (hace que la web cargue rápido y comprime archivos)
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================
# CONFIGURACIÓN DE SEGURIDAD Y SESIONES
# ==========================================

# 1. Cierra la sesión automáticamente al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 2. Tiempo máximo de inactividad (en segundos). Ejemplo: 900 = 15 minutos
SESSION_COOKIE_AGE = 3600 

# 3. Renueva el temporizador cada vez que el usuario hace clic en algo
SESSION_SAVE_EVERY_REQUEST = True

# 4. Le dice a Django a dónde enviar a la gente si su sesión expira o intentan 
# entrar a una página prohibida sin iniciar sesión
LOGIN_URL = 'login'

# A dónde ir después de iniciar sesión con éxito (al catálogo)
LOGIN_REDIRECT_URL = 'index' 

# A dónde ir después de cerrar sesión (a la portada pública)
LOGOUT_REDIRECT_URL = 'landing'