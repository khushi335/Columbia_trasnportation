import os
import sys

# Add your project directory to the sys.path
sys.path.insert(0, '/home/hightech/columbiatransportation.com/service')

# Activate the virtual environment
activate_this = '/home/hightech/virtualenv/columbiatransportation.com/service/3.10/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'service.settings'

# Import and set up the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
