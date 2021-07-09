# Production settings
from moth_api.settings.common import *

from conf.secrets import DOMAIN, USER_DIR


DEBUG = False


ALLOWED_HOSTS = [SERVER_IP, DOMAIN, f'www.{DOMAIN}']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = f'{USER_DIR}/static/'
STATIC_URL = '/static/'
MEDIA_ROOT = f'{USER_DIR}/media/images/'
MEDIA_URL = '/media/images/'


# HTTPS Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
