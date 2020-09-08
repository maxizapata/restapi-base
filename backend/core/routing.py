# from django.urls import path

# from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from .channels_middleware import TokenAuthMiddleware
from trips.routing import trips_ws_urlpatterns


application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddleware(
        URLRouter(
            trips_ws_urlpatterns
        ),
    ),

})