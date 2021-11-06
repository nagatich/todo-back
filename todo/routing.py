from django.urls import path

from channels.routing import URLRouter

from notifications.consumers import NotificationConsumer
from core.routing import websocket_urlpatterns as core_routing

websocket_urlpatterns = URLRouter([
    path('notifications/', NotificationConsumer.as_asgi()),
    path('', core_routing),
])
