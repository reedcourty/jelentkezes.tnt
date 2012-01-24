import os
import sys

paths = ['/home/reedcourty_l/jelentkezes.tnt',
        '/home/reedcourty_l/jelentkezes.tnt/jelentkezes',]

for p in paths:
    if p not in sys.path:
        sys.path.append(p)

os.environ['DJANGO_SETTINGS_MODULE'] = 'jelentkezes.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
