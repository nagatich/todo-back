import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
django_asgi_app = get_asgi_application()

from notifications.middleware import AuthMiddleware

from .routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AuthMiddleware(websocket_urlpatterns),
})
