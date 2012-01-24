import os
import sys

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit("/",2)[0]

paths = [PROJECT_PATH, PROJECT_PATH + '/jelentkezes',]

for p in paths:
    if p not in sys.path:
        sys.path.append(p)

os.environ['DJANGO_SETTINGS_MODULE'] = 'jelentkezes.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
