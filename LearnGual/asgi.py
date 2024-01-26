import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LearnGual.settings")

django.setup()
asgi_app = get_asgi_application()

# pylint: disable-next=wrong-import-position
from app.routing import websocket_urlpatterns

# pylint: disable-next=wrong-import-position
from app.middlewares import TokenAuthMiddleWare


application = ProtocolTypeRouter(
    {
        "http": asgi_app,
        "websocket": TokenAuthMiddleWare(
            URLRouter(
                websocket_urlpatterns,
            ),
        ),
    }
)
