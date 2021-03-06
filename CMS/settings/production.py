import sys, logging, watchtower

from .base import *


DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

AWS_DISTRIBUTION_ID = os.environ.get('DISTRIBUTION_ID')
AWS_DOWNLOAD_DISTRIBUTION_ID = os.environ.get('DOWNLOAD_DISTRIBUTION_ID')

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

# Bakery settings

BAKERY_VIEWS = (
    'wagtailbakery.views.AllPublishedPagesView',
    'static_views.views.SitemapView',
)

# File upload settings

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# max in-memory size for s3 uploads. Anything bigger than this rolled over into a temp file.
AWS_S3_MAX_MEMORY_SIZE = os.environ.get('AWS_S3_MAX_MEMORY_SIZE', int(2.5 * 1000000)) # default 2.5MB

# Site deployment settings

AWS_ACCESS_KEY_ID_DEPLOYMENT = os.environ.get('AWS_ACCESS_KEY_ID_DEPLOYMENT')
AWS_SECRET_ACCESS_KEY_DEPLOYMENT = os.environ.get('AWS_SECRET_ACCESS_KEY_DEPLOYMENT')
AWS_STORAGE_BUCKET_NAME_DEPLOYMENT = os.environ.get('AWS_STORAGE_BUCKET_NAME_DEPLOYMENT')
AWS_REGION_DEPLOYMENT = os.environ.get('AWS_REGION_DEPLOYMENT', 'eu-west-1')

# Security settings

SECURE_HSTS_SECONDS = os.environ.get('SECURE_HSTS_SECONDS', 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# Email notification config
DEFAULT_FROM_EMAIL = os.environ.get('FROM_EMAIL', 'partnerships@phe.gov.uk')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'email-smtp.eu-west-1.amazonaws.com')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
EMAIL_USE_TLS = True 
EMAIL_SUBJECT_PREFIX = '[Coronavirus Resources ] '
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = os.environ.get('FROM_EMAIL', 'partnerships@phe.gov.uk')
WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = False

ATHENA_WORKGROUP = os.environ.get('ATHENA_WORKGROUP', 'primary')
ATHENA_OUTPUT_BUCKET = os.environ.get('ATHENA_OUTPUT_BUCKET')


try:
    from .local import *
except ImportError:
    pass
