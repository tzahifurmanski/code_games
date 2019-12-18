"""
WSGI config for analysis_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import logging


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analysis_server.settings')
logging.basicConfig(level="DEBUG")

application = get_wsgi_application()
