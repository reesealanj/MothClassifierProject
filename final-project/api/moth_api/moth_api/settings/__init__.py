import os

if os.environ.get('production', 'false') == 'true':
    from moth_api.settings.production import *
else:
    from moth_api.settings.development import *
