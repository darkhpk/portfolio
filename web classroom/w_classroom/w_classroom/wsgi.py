"""
WSGI config for web_classroom project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'w_classroom.settings')

application = get_wsgi_application()
