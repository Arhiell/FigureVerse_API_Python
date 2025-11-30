from pathlib import Path
import os
import firebase_admin
from firebase_admin import credentials, firestore

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_PATH):
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                k, sep, v = s.partition("=")
                if sep:
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass

FIREBASE_CREDENTIALS = (
    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    or os.environ.get("FIREBASE_CREDENTIALS_PATH")
    or os.environ.get("FIREBASE_CREDENTIALS")
    or os.path.join(BASE_DIR, "serviceAccountKey.json")
)
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = FIREBASE_CREDENTIALS
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID")
if os.path.exists(FIREBASE_CREDENTIALS):
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)
    FIRESTORE_DB = firestore.client()
else:
    FIRESTORE_DB = None

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') if os.environ.get('DJANGO_ALLOWED_HOSTS') else []

#Configurar la URL base de las Cloud Functions
CLOUD_FUNCTIONS_EMULATOR_BASE_URL = os.environ.get(
    "CLOUD_FUNCTIONS_EMULATOR_BASE_URL",
    "http://localhost:5001/figureverse-9b12e/us-central1/api",
)
CLOUD_FUNCTIONS_BASE_URL = os.environ.get(
    "CLOUD_FUNCTIONS_BASE_URL",
    CLOUD_FUNCTIONS_EMULATOR_BASE_URL if DEBUG else "https://api-pcjssvdena-uc.a.run.app",
)
CLOUD_FUNCTIONS_TIMEOUT = int(os.environ.get("CLOUD_FUNCTIONS_TIMEOUT", "10"))
CLOUD_FUNCTIONS_AUTH_TOKEN = os.environ.get("CLOUD_FUNCTIONS_AUTH_TOKEN")
CLOUD_FUNCTIONS_FUNCTION_NAME = os.environ.get("CLOUD_FUNCTIONS_FUNCTION_NAME", "api")
CLOUD_FUNCTIONS_VERIFY_TLS = os.environ.get("CLOUD_FUNCTIONS_VERIFY_TLS", "True") == "True"
CLOUD_FUNCTIONS_FALLBACK_BASE_URL = os.environ.get(
    "CLOUD_FUNCTIONS_FALLBACK_BASE_URL",
    "https://us-central1-figureverse-9b12e.cloudfunctions.net/api",
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
      # Apps de terceros
    'rest_framework',
    # Nuestra app
    'feedback',
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

ROOT_URLCONF = 'ai_reviews_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai_reviews_api.wsgi.application'


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

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
