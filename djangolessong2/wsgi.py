"""
WSGI config for djangolessong2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangolessong2.settings')
application=Cling(get_wsgi_application())
application = get_wsgi_application()
if not settings.DEBUG:
    try:
        from dj_static import Cling
        application = Cling(get_wsgi_application())
    except:
        pass