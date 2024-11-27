from __future__ import annotations
from typing import TYPE_CHECKING, Union, Optional

from django.db import transaction
from django.utils import timezone
from djoser import signals
from djoser.conf import settings

from users.views import users as users_views
from users.services.tasks import tasks

if TYPE_CHECKING:
    from users.models.users import User
    from users.serializers.api.users import CustomPasswordResetConfirmSerializer


class UserSignalActivationService:
    """Service for handling user activation signals."""

    def __init__(self, user: User) -> None:
        """Initialize the user activation signal service."""
        self._user = user

    def signal_user_activation(self) -> None:
        """Send the user activation signal."""
        signals.user_activated.send(
            sender=users_views.CustomUserViewSet,
            user=self._user,
            request=users_views.CustomUserViewSet.request,
        )


class UserRegistrationService(UserSignalActivationService):
    """Service for handling user registration."""

    def __init__(self, user: User, context: Optional[dict[str, Union[str, int]]]) -> None:
        """Initialize the user registration service."""
        super().__init__(user)
        self._context = context


    def _send_welcome_email(self) -> None:
        """Send welcome email"""
        tasks.send_welcome_email_task.delay(self._user.email)

    def execute(self) -> None:
        """Running"""
        self._send_welcome_email()

#
# class UserActivationService(UserSignalActivationService):
#     """Service for handling user activation."""
#
#     def __init__(self, user: User, context: Optional[dict[str, Union[str, int]]]) -> None:
#         """Initialize the user activation service."""
#         super().__init__(user)
#         self._context = context
#
#     def _user_is_active(self) -> None:
#         """Mark the user as active."""
#         self._user.is_active = True
#
#     def _user_save(self) -> None:
#         """Save the user."""
#         self._user.save()
#
#     def _send_email_user_activation(self):
#         """Send an email about user activation."""
#         tasks.send_activation_task.delay(self._context, [self._user.email])
#
#     def execute(self) -> None:
#         """Execute user activation."""
#         with transaction.atomic():
#             self._user_is_active()
#             self._user_save()
#
#         self.signal_user_activation()
#         if settings.SEND_CONFIRMATION_EMAIL:
#             self._send_email_user_activation()


class UserResetPasswordService:
    """Service for requesting a new password."""

    def __init__(self, user: User, context: Optional[dict[str, Union[str, int]]]) -> None:
        """Initialize the password reset service."""
        self._user = user
        self._context = context

    def _send_email_user_reset_password(self) -> None:
        """Send an email for resetting the password."""
        tasks.send_reset_password_task.delay(self._context, [self._user.email])

    def execute(self) -> None:
        """Execute the password reset process."""
        if self._user:
            self._send_email_user_reset_password()


class UserResetPasswordConfirmService:
    """Service for resetting and setting a new password."""

    def __init__(
        self,
        user: User,
        serializer: CustomPasswordResetConfirmSerializer,
        context: Optional[dict[str, Union[str, int]]],
    ) -> None:
        """Initialize the password reset confirmation service."""
        self._user = user
        self._serializer = serializer
        self._context = context

    def _set_password(self) -> None:
        """Set a new password."""
        self._user.set_password(self._serializer.data['new_password'])

    def _is_has_last_login(self) -> None:
        """Update the `last_login` attribute if it exists."""
        if hasattr(self._user, 'last_login'):
            self._user.last_login = timezone.now()

    def _user_save(self) -> None:
        """Save the user."""
        self._user.save()

    def _send_email_user_reset_password_confirm(self) -> None:
        """Send an email about password reset confirmation."""
        tasks.send_reset_password_confirm_task.delay(
            self._context, [self._user.email]
        )

    def execute(self):
        """Execute the password reset confirmation process."""
        with transaction.atomic():
            self._set_password()
            self._is_has_last_login()
            self._user_save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            self._send_email_user_reset_password_confirm()
