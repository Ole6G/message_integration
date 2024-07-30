import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from email_integration.routing import websocket_urlpatterns

# Устанавливаем переменную окружения на настройки вашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_integration.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})