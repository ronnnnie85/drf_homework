import os

from dotenv import load_dotenv
from rest_framework.permissions import SAFE_METHODS, BasePermission

load_dotenv()
MOD_GROUP = os.getenv("MOD_GROUP")


class ModeratorsNoCreateDelete(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        is_moderator = user.groups.filter(name=MOD_GROUP).exists()

        if is_moderator and request.method in ("POST", "DELETE"):
            return False

        return True


class OwnerOnlyForNonModerators(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_moderator = user.groups.filter(name=MOD_GROUP).exists()
        if is_moderator:
            return True

        return getattr(obj, "owner_id", None) == user.id
