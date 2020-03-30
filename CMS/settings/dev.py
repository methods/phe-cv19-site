from .base import *

from CMS.settings.management_cron_jobs import schedule_cron_jobs

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3z@sut7t&=hkx9*+b-h=&2$_ajcqvqrfcc0mc@*)y6c5v#6qsz'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Bakery settings

BAKERY_VIEWS = (
    'wagtailbakery.views.AllPublishedPagesView',
)

# Site deployment settings

AWS_ACCESS_KEY_ID_DEPLOYMENT = os.environ.get('AWS_ACCESS_KEY_ID_DEPLOYMENT')
AWS_SECRET_ACCESS_KEY_DEPLOYMENT = os.environ.get('AWS_SECRET_ACCESS_KEY_DEPLOYMENT')
AWS_STORAGE_BUCKET_NAME_DEPLOYMENT = os.environ.get('AWS_STORAGE_BUCKET_NAME_DEPLOYMENT')
AWS_REGION_DEPLOYMENT = os.environ.get('AWS_REGION_DEPLOYMENT')

try:
    from .local import *
except ImportError:
    pass
