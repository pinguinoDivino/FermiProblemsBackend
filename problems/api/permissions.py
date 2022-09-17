from django.contrib.auth import get_user_model
from rest_framework import permissions
from problems.models import Problem, ProblemValidationByUser
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = _("Only the author can update or delete")

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Problem):
            return obj.author == request.user


class IsAuthorOrNotAllowed(permissions.BasePermission):
    message = _("Only author can visualize or do actions")

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, ProblemValidationByUser):
            return obj.problem.user == request.user
