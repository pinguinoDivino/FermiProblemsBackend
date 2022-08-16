from django.contrib.auth import get_user_model
from rest_framework import permissions
from .serializers import error_messages
User = get_user_model()


class IsUser(permissions.BasePermission):
    message = error_messages['not_authorized']

    def has_object_permission(self, request, view, obj):
        return obj == request.user

