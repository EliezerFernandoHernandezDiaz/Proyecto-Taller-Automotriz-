"""
Django settings for login project.
"""

from pathlib import Path
import os
import dj_database_url

# --- Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core
SECRET_KEY = os.getenv("SECRET_KEY", "clave-respaldo")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Si Render expone el hostname vía env, agrégalo a ALLOWED_HOSTS y CSRF
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST and RENDER_HOST not in ALLOWED_HOSTS:
    ALLOWED_HOSTS += [RENDER_HOST]
CSRF_TRUSTED_ORIGINS = [
    *(os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")),
    # agrega tu dominio de Render si quieres forzarlo aquí:
    "https://proyecto-taller-automotriz.onrender.com",
]
CSRF_TRUSTED_ORIGINS = [o for o in CSRF_TRUSTED_ORIGINS if o]  # limpia vacíos

# --- Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "accounts",
    "cloudinary",
    "cloudinary_storage",
]

# --- Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "login.urls"

# --- Templates
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

WSGI_APPLICATION = "login.wsgi.application"

# --- DB
if os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            env="DATABASE_URL",
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- Passwords
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- I18N
LANGUAGE_CODE = "es-es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# si tienes carpeta 'static' local, déjala; si no existe, puedes quitar esta línea
STATICFILES_DIRS = [BASE_DIR / "static"]

# --- Media (no se usa con Cloudinary pero no estorba)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Cloudinary
# Puedes usar o bien CLOUDINARY_URL (recomendado) o las 3 variables por separado.
# CLOUDINARY_URL formato: cloudinary://API_KEY:API_SECRET@CLOUD_NAME
from cloudinary import config as cloudinary_config

if os.getenv("CLOUDINARY_URL"):
    cloudinary_config(secure=True)  # usa CLOUDINARY_URL directamente
else:
    cloudinary_config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )

# Django 4.2+/5.x: STORAGES
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# --- Misc/Prod
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # útil en Render
