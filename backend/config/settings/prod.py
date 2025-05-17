from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# STATIC
# ------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
