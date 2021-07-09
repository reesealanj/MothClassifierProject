# Development settings
from moth_api.settings.common import *


STATIC_URL = '/static/'
MEDIA_ROOT = '/mnt/volume_nyc3_01/images/'
MEDIA_URL = f'/{Path(MEDIA_ROOT).name}/'
