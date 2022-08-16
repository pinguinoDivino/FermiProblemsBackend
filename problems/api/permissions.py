from django.contrib.auth import get_user_model
from rest_framework import permissions
from ..models import Problem

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = "Solo l'autore può modificare o cancellare il proprio post"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Problem):
            return obj.author == request.user
