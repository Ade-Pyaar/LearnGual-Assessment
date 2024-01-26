from django.urls import path

from app.consumers import ChatConsumer


websocket_urlpatterns = [
    path("chat/", ChatConsumer.as_asgi()),
]
