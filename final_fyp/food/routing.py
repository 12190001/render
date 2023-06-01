from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'wss://gofoodie-1a86.onrender.com/ws/notifications/', consumers.NotificationConsumer.as_asgi()),

]

