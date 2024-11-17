"""
ASGI config for phone_store project.

It exposes the ASGI callable as a module-level variable named ``applications``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phone_store.settings")

application = get_asgi_application()
