import functools
from .models import MultiplayerGame
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async


def UseMultiplayerGame(func, obj_id):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        obj = await database_sync_to_async(get_object_or_404)(MultiplayerGame, pk=obj_id)
        return await func(obj, *args, **kwargs)
    return wrapper
