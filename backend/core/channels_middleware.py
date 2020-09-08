from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack


@database_sync_to_async
def get_user(user_id):
    try:
        return get_user_model().objects.get(id=user_id)
    except get_user_model().DoNotExist:
        return AnonymousUser()


class QueryAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = scope
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        close_old_connections()
        token = parse_qs(
            self.scope["query_string"].decode("utf8"))["token"][0]
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError):
            self.scope['user'] = AnonymousUser()
        else:
            decoded_data = jwt_decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            self.scope['user'] = await get_user(
                decoded_data['user_id'])
        inner = self.inner(self.scope)
        return await inner(receive, send)


class QueryAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        return QueryAuthMiddlewareInstance(scope, self)


TokenAuthMiddleware = lambda inner: QueryAuthMiddleware(AuthMiddlewareStack(inner))

