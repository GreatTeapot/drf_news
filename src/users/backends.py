

from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.request import Request

User = get_user_model()


class AuthBackend(object):
    """
    Backend authentication.
    
    Attributes:
        * `supports_object_permissions` (bool): supports object permissions.
        * `supports_anonymous_user` (bool): supports anonymous users.
        * `supports_inactive_user` (bool): supports inactive users.
    """

    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        """Get user by ID."""

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def authenticate(
            request: Request,
            username: str,
            password: str,
    ) -> Optional[User]:
        """Check one of the authentication choices and password."""

        try:
            user = User.objects.get(
                Q(username=username) |
                Q(email=username) |
                Q(phone_number=username)
            )
        except User.DoesNotExist:
            return None
        return user if user.check_password(password) else None
