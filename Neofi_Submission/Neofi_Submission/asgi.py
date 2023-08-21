"""
ASGI config for Neofi_Submission project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/

# isort: skip_file
"""
import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Neofi_Submission.settings')
django_asgi_app = get_asgi_application()


from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from chatapp.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter(websocket_urlpatterns),
})
