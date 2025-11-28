"""
WSGI config for movie_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_backend.settings')

application = get_wsgi_application()

# Serve static files with WhiteNoise
application = WhiteNoise(application)
application.add_files(os.path.join(os.path.dirname(__file__), '..', 'staticfiles'), prefix='/static/')