from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from email_integration import consumers

websocket_urlpatterns = [
    path('ws/email/', consumers.EmailConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns)
})
