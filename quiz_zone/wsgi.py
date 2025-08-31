import sys
import os

# Add project folder to sys.path
path = '/home/rafsunjany/Quiz-Zone'
if path not in sys.path:
    sys.path.append(path)

# Activate virtualenv
activate_this = '/home/rafsunjany/Quiz-Zone/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_zone.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

