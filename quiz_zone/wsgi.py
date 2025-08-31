import sys
import os

# add your project folder to the sys.path
path = '/home/rafsunjany/Quiz-Zone'
if path not in sys.path:
    sys.path.append(path)

# set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_zone.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
