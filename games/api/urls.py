from django.urls import path
from . import views

urlpatterns = [
    path("games/multiplayer/start/", views.StartMultiplayerGameApiView.as_view())
]