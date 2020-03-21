import sys

from .base import *

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    # add the site domain name in here
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './debug.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

WAGTAILFRONTENDCACHE = {
    'cloudflare': {
        'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudflareBackend',
        'EMAIL': os.environ.get('CLOUDFLARE_EMAIL'),
        'TOKEN': os.environ.get('CLOUDFLARE_TOKEN'),
        'ZONEID': os.environ.get('CLOUDFLARE_ZONEID'),
    },
}

# Bakery settings

BAKERY_VIEWS = (
    'wagtailbakery.views.AllPublishedPagesView',
)

# File upload settings

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')    # eg. 'campaignstorage'
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')      # eg. '<secret key>'
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER')          # eg. 'campaign-resource-centre'

# Security settings

SECURE_HSTS_SECONDS = os.environ.get('SECURE_HSTS_SECONDS', 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

try:
    from .local import *
except ImportError:
    pass
