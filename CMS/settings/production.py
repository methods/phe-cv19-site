import sys

from .base import *

from CMS.settings.management_cron_jobs import schedule_cron_jobs

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

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# Site deployment settings

AWS_ACCESS_KEY_ID_DEPLOYMENT = os.environ.get('AWS_ACCESS_KEY_ID_DEPLOYMENT')
AWS_SECRET_ACCESS_KEY_DEPLOYMENT = os.environ.get('AWS_SECRET_ACCESS_KEY_DEPLOYMENT')
AWS_STORAGE_BUCKET_NAME_DEPLOYMENT = os.environ.get('AWS_STORAGE_BUCKET_NAME_DEPLOYMENT')
AWS_REGION_DEPLOYMENT = os.environ.get('AWS_REGION_DEPLOYMENT')

# Security settings

SECURE_HSTS_SECONDS = os.environ.get('SECURE_HSTS_SECONDS', 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# cron

SCHEDULE_CRON_JOBS = os.environ.get('SCHEDULE_CRON_JOBS')
if SCHEDULE_CRON_JOBS.lower() == 'true':
    schedule_cron_jobs()


try:
    from .local import *
except ImportError:
    pass
