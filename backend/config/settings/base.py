"""
Base settings to build other settings files upon.
"""

from pathlib import Path

import environ

from application.__init__ import __version__

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# application/
APPS_DIR = ROOT_DIR / "application"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", env("ALLOWED_HOSTS")]

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "CET"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

if env("DATABASE_ENGINE") == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ATOMIC_REQUESTS": True,
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": env.str("DATABASE_DB", "/var/lib/sqlite/secobserve.db"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ATOMIC_REQUESTS": True,
            "ENGINE": env("DATABASE_ENGINE"),
            "HOST": env("DATABASE_HOST"),
            "PORT": env("DATABASE_PORT"),
            "NAME": env("DATABASE_DB"),
            "USER": env("DATABASE_USER"),
            "PASSWORD": env("DATABASE_PASSWORD"),
        }
    }

    if env("DATABASE_ENGINE") == "django.db.backends.mysql":
        DATABASES["default"]["OPTIONS"] = {"charset": "utf8mb4"}
        if env("MYSQL_AZURE", default="false") == "single":
            DATABASES["default"]["OPTIONS"]["ssl"] = {
                "ca": "/app/BaltimoreCyberTrustRoot_combined.crt.pem"
            }
        if env("MYSQL_AZURE", default="false") == "flexible":
            DATABASES["default"]["OPTIONS"]["ssl"] = {
                "ca": "/app/DigiCertGlobalRootCA.crt.pem"
            }

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_filters",
    "constance",
    "constance.backends.database",
    "huey.contrib.djhuey",
]

LOCAL_APPS = [
    "application.access_control",
    "application.commons",
    "application.core",
    "application.epss",
    "application.import_observations",
    "application.issue_tracker",
    "application.metrics",
    "application.rules",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "access_control.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Deactivated LocaleMiddleware to ensure English messages
    # "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
    "application.commons.services.global_request.GlobalRequestMiddleware",
    "application.commons.services.security_headers.SecurityHeadersMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(APPS_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/django-static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


def whitenoise_security_headers(headers, path, url):
    headers["Permissions-Policy"] = "geolocation=() camera=(), microphone=()"


# https://whitenoise.evans.io/en/stable/django.html#WHITENOISE_ADD_HEADERS_FUNCTION
WHITENOISE_ADD_HEADERS_FUNCTION = whitenoise_security_headers

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-age
SESSION_COOKIE_AGE = 86400  # 1 day in seconds
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-samesite
SESSION_COOKIE_SAMESITE = "Strict"
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-samesite
CSRF_COOKIE_SAMESITE = "Strict"
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = False
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"
# https://django-csp.readthedocs.io/en/latest/configuration.html
CSP_SCRIPT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'none'",)
CSP_FRAME_ANCESTORS = ("'self'",)
CSP_FORM_ACTION = ("'self'",)
# https://docs.djangoproject.com/en/dev/ref/middleware/#http-strict-transport-security
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-referrer-policy
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = env("EMAIL_PORT", default=1025)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=False)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("admin", "admin@example.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s | %(asctime)s | %(name)s | "
            "%(process)d %(thread)d | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # },
        # 'django_auth_adfs': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # },
        "werkzeug": {
            "handlers": ["console"],
            "level": "CRITICAL",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "CRITICAL",
        },
        "huey": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    },
}

# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
# -------------------------------------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------------------------------------
if env("OIDC_AUTHORITY"):
    DEFAULT_AUTHENTICATION_CLASSES = [
        "application.access_control.services.oidc_authentication.OIDCAuthentication",
        "application.access_control.services.api_token_authentication.APITokenAuthentication",
        "application.access_control.services.jwt_authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ]
else:
    DEFAULT_AUTHENTICATION_CLASSES = [
        "application.access_control.services.api_token_authentication.APITokenAuthentication",
        "application.access_control.services.jwt_authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "application.commons.utils.PageNumberWithPageSizePagination",
    "PAGE_SIZE": 25,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "10/second", "user": "100/second"},
    "EXCEPTION_HANDLER": "commons.api.exception_handler.custom_exception_handler",
}

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
# CORS_URLS_REGEX = r"^/api/.*$"

# Your stuff...
# ------------------------------------------------------------------------------

SPECTACULAR_SETTINGS = {
    "TITLE": "SecObserve",
    "DESCRIPTION": "...",
    "VERSION": __version__,
    # show file selection dialogue, see https://github.com/tfranzel/drf-spectacular/issues/455
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SWAGGER_UI_SETTINGS": {"docExpansion": "none"},
    "ENUM_GENERATE_CHOICE_DESCRIPTION": False,
}

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = {
    "SECURITY_GATE_ACTIVE": (True, "Is the security gate activated?", bool),
    "SECURITY_GATE_THRESHOLD_CRITICAL": (
        0,
        "Number of critical observations that must not be exceeded",
        int,
    ),
    "SECURITY_GATE_THRESHOLD_HIGH": (
        0,
        "Number of high observations that must not be exceeded",
        int,
    ),
    "SECURITY_GATE_THRESHOLD_MEDIUM": (
        99999,
        "Number of medium observations that must not be exceeded",
        int,
    ),
    "SECURITY_GATE_THRESHOLD_LOW": (
        99999,
        "Number of low observations that must not be exceeded",
        int,
    ),
    "SECURITY_GATE_THRESHOLD_NONE": (
        99999,
        "Number of none observations that must not be exceeded",
        int,
    ),
    "SECURITY_GATE_THRESHOLD_UNKOWN": (
        99999,
        "Number of unkown observations that must not be exceeded",
        int,
    ),
    "JWT_VALIDITY_DURATION_USER": (
        168,
        "Validity duration of JWT tokens for regular users in hours",
        int,
    ),
    "JWT_VALIDITY_DURATION_SUPERUSER": (
        24,
        "Validity duration of JWT tokens for superusers in hours",
        int,
    ),
    "BASE_URL_FRONTEND": (
        "",
        "Base URL of the frontend, used to set links in notifications correctly",
        str,
    ),
    "EXCEPTION_MS_TEAMS_WEBHOOK": (
        "",
        "MS Teams webhook to send exception notifications",
        str,
    ),
    "EXCEPTION_SLACK_WEBHOOK": (
        "",
        "Slack webhook to send exception notifications",
        str,
    ),
    "EXCEPTION_RATELIMIT": (
        3600,
        "Timedelta in seconds when to send the same exception the next time",
        int,
    ),
    "EMAIL_FROM": (
        "",
        "From address for sending email notifications",
        str,
    ),
    "EXCEPTION_EMAIL_TO": (
        "",
        "Comma separated email addresses to send exception notifications",
        str,
    ),
    "BACKGROUND_PRODUCT_METRICS_INTERVAL_MINUTES": (
        5,
        "Calculate product metrics every x minutes",
        int,
    ),
    "BACKGROUND_EPSS_IMPORT_CRONTAB_MINUTES": (
        "0",
        "Minutes crontab expression for EPSS import",
        str,
    ),
    "BACKGROUND_EPSS_IMPORT_CRONTAB_HOURS": (
        "3",
        "Hours crontab expression for EPSS import (UTC)",
        str,
    ),
    "BRANCH_HOUSEKEEPING_CRONTAB_MINUTES": (
        "0",
        "Minutes crontab expression for branch housekeeping",
        str,
    ),
    "BRANCH_HOUSEKEEPING_CRONTAB_HOURS": (
        "2",
        "Hours crontab expression for branch housekeeping (UTC)",
        str,
    ),
    "BRANCH_HOUSEKEEPING_ACTIVE": (
        True,
        "Delete inactive branches",
        bool,
    ),
    "BRANCH_HOUSEKEEPING_KEEP_INACTIVE_DAYS": (
        30,
        "Days before incative branches and their observations are deleted",
        int,
    ),
    "BRANCH_HOUSEKEEPING_EXEMPT_BRANCHES": (
        "",
        "Regular expression which branches to exempt from deletion",
        str,
    ),
}

CONSTANCE_CONFIG_FIELDSETS = {
    "Security Gate": (
        "SECURITY_GATE_ACTIVE",
        "SECURITY_GATE_THRESHOLD_CRITICAL",
        "SECURITY_GATE_THRESHOLD_HIGH",
        "SECURITY_GATE_THRESHOLD_MEDIUM",
        "SECURITY_GATE_THRESHOLD_LOW",
        "SECURITY_GATE_THRESHOLD_NONE",
        "SECURITY_GATE_THRESHOLD_UNKOWN",
    ),
    "Authentication": (
        "JWT_VALIDITY_DURATION_USER",
        "JWT_VALIDITY_DURATION_SUPERUSER",
    ),
    "Integrations": (
        "BASE_URL_FRONTEND",
        "EMAIL_FROM",
        "EXCEPTION_EMAIL_TO",
        "EXCEPTION_MS_TEAMS_WEBHOOK",
        "EXCEPTION_SLACK_WEBHOOK",
        "EXCEPTION_RATELIMIT",
    ),
    "Background tasks (restart needed)": (
        "BACKGROUND_PRODUCT_METRICS_INTERVAL_MINUTES",
        "BACKGROUND_EPSS_IMPORT_CRONTAB_MINUTES",
        "BACKGROUND_EPSS_IMPORT_CRONTAB_HOURS",
    ),
    "Housekeeping for branches": (
        "BRANCH_HOUSEKEEPING_CRONTAB_MINUTES",
        "BRANCH_HOUSEKEEPING_CRONTAB_HOURS",
        "BRANCH_HOUSEKEEPING_ACTIVE",
        "BRANCH_HOUSEKEEPING_KEEP_INACTIVE_DAYS",
        "BRANCH_HOUSEKEEPING_EXEMPT_BRANCHES",
    ),
}

FIELD_ENCRYPTION_KEY = env("FIELD_ENCRYPTION_KEY")

HUEY_FILENAME = env("HUEY_FILENAME", default="/var/lib/huey/huey.db")

HUEY = {
    "huey_class": "huey.SqliteHuey",  # Huey implementation to use.
    "name": DATABASES["default"]["NAME"],  # Use db name for huey.
    "results": False,  # Store return values of tasks.
    "store_none": False,  # If a task returns None, do not save to results.
    "immediate": DEBUG,  # If DEBUG=True, run synchronously.
    "utc": True,  # Use UTC for all times internally.
    "connection": {
        "filename": HUEY_FILENAME,  # Filename for sqlite.
    },
    "consumer": {
        "workers": 2,
        "worker_type": "thread",
        "initial_delay": 0.1,  # Smallest polling interval, same as -d.
        "backoff": 1.15,  # Exponential backoff using this rate, -b.
        "max_delay": 10.0,  # Max possible polling interval, -m.
        "scheduler_interval": 1,  # Check schedule every second, -s.
        "periodic": True,  # Enable crontab feature.
        "check_worker_health": True,  # Enable worker health checks.
        "health_check_interval": 60,  # Check worker health every second.
    },
}
