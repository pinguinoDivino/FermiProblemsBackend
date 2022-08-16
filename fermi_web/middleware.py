from django.contrib.auth.models import AnonymousUser
from knox.models import AuthToken
from knox.settings import CONSTANTS
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack


@database_sync_to_async
def get_user(token_key):
    # If you are using normal token based authentication
    try:
        knox_object = AuthToken.objects.filter(token_key=token_key[:CONSTANTS.TOKEN_KEY_LENGTH]).first()
        return knox_object.user
    except AuthToken.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)


def TokenAuthMiddlewareStack(inner): return TokenAuthMiddleware(
    AuthMiddlewareStack(inner))

# TODO auth with session to add
