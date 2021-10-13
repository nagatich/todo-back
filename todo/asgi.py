from channels.routing import ProtocolTypeRouter

from notifications.middleware import AuthMiddleware

from .routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': AuthMiddleware(websocket_urlpatterns),
})
