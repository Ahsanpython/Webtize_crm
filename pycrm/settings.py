# D:\pycrm\pycrm\settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------
def env_bool(name: str, default: str = "False") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}

def env_list(name: str, default_csv: str):
    # split comma-separated env var -> list[str] (stripped)
    return [h.strip() for h in os.getenv(name, default_csv).split(",") if h.strip()]

# --------------------------------------------------------------------------------------
# Core
# --------------------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-please-change")

# DEBUG: True locally, False on server (set DEBUG=0 in PythonAnywhere env)
DEBUG = env_bool("DEBUG", "True")

# Hosts & CSRF (includes local + PythonAnywhere by default)
ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,.pythonanywhere.com"
)

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://127.0.0.1,http://localhost,https://*.pythonanywhere.com"
)

# --------------------------------------------------------------------------------------
# Installed apps
# --------------------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "django_filters",

    # local apps
    "performance",
    "clients",
    "projects",
    "timesheets",
    "invoices",
    "dashboard",
    "expenses",
]

# --------------------------------------------------------------------------------------
# Middleware / URLs / Templates / WSGI
# --------------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pycrm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pycrm.wsgi.application"

# --------------------------------------------------------------------------------------
# Database (SQLite is fine on PythonAnywhere free; the file persists)
# --------------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --------------------------------------------------------------------------------------
# Auth / i18n / tz
# --------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Karachi"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------------------
# Static files
# --------------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]         # your local assets
STATIC_ROOT = BASE_DIR / "staticfiles"           # where collectstatic puts files (PA maps /static/ -> this folder)

# --------------------------------------------------------------------------------------
# REST Framework
# --------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# --------------------------------------------------------------------------------------
# Security for production (PythonAnywhere)
# --------------------------------------------------------------------------------------
if not DEBUG:
    # Redirect all HTTP -> HTTPS (you can disable with SECURE_SSL_REDIRECT=0)
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", "True")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS off by default on shared hosting; enable if you own the domain and use HTTPS only
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
