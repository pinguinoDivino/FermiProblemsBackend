"""
ASGI config for fermi_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from fermi_web.middleware import TokenAuthMiddleware  # middleware custom Token auth
import games.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fermi_website.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(TokenAuthMiddleware(
        URLRouter(
            games.routing.websocket_urlpatterns
        )
    ))
})
