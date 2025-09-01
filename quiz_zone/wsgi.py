import os
import sys

<<<<<<< HEAD
# Add project folder to sys.path
path = '/home/rafsunjany/Quiz-Zone'
if path not in sys.path:
    sys.path.append(path)

# Activate virtualenv
activate_this = '/home/rafsunjany/Quiz-Zone/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

=======
# Add project directory to Python path
project_home = '/home/Rafsunjany/Quiz-Zone/venv'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

>>>>>>> b1d7eca (Adding Ratting option for user and responsive UI with auth)
# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_zone.settings')

# Activate virtualenv
# Not needed for Python 3.10 venv, PythonAnywhere uses the virtualenv path from the Web tab

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

