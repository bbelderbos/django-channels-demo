import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chat.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP requests
    "websocket": AuthMiddlewareStack(  # WebSocket requests
        URLRouter(websocket_urlpatterns)  # WebSocket routing
    ),
})

