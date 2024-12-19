
from typing import TypeAlias
from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.conf import settings
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, status, authentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt import authentication as jwt_authentication

from djoser import permissions as djoser_permissions
from config import settings as app_settings
from common.views import mixins
from users.serializers.api import users as user_s
from users.services import users as users_services
from users.services.utils import get_context

User = get_user_model()

RegistrationSerializer: TypeAlias = user_s.RegistrationSerializer


@extend_schema_view(
    registration=extend_schema(
        summary='User registration',
        tags=['Registration'],
    ),
    reset_password=extend_schema(
        summary='Request for a new password via email',
        tags=['Registration'],
    ),
    change_password=extend_schema(
        summary='Change password',
        tags=['Authorization'],
    ),
    activation=extend_schema(
        summary='User activation',
        tags=['Authorization'],
    ),
    reset_password_confirm=extend_schema(
        summary='Password reset',
        tags=['Authorization'],
    ),
    me=extend_schema(
        summary='User profile',
        tags=['User'],
    ),
    edit=extend_schema(
        summary='Partially update user profile',
        tags=['User'],
    ),
    edit_role=extend_schema(
        summary='Update user role',
        tags=['User']
    )
)
class CustomUserViewSet(mixins.ExtendedUserViewSet):
    """
    User view.
    This view includes user authorization and registration.
    It also includes user information and modifications.
    """
    queryset = User.objects.all()

    authentication_classes = (jwt_authentication.JWTAuthentication,)
    multi_authentication_classes = {
        'registration': (authentication.BasicAuthentication,),
        'activation': (authentication.BasicAuthentication,),
    }

    permission_classes = (djoser_permissions.CurrentUserOrAdmin,)
    multi_permission_classes = {
        'registration': (permissions.AllowAny,),
        # 'activation': (permissions.AllowAny,),
        'edit_role': (permissions.IsAdminUser,),
    }

    serializer_class = user_s.UserSerializer
    multi_serializer_class = {
        'registration': user_s.RegistrationSerializer,
        # 'activation': user_s.CustomActivationSerializer,
        'change_password': user_s.ChangePasswordSerializer,
        'reset_password': user_s.PasswordResetSerializer,
        'reset_password_confirm': user_s.CustomPasswordResetConfirmSerializer,
        'me': user_s.UserSerializer,
        'edit': user_s.UserUpdateSerializer,
        'edit_role': user_s.UserUpdateRoleSerializer,
    }

    def get_object(self) -> User:
        """Retrieve the user object"""
        return self.request.user

    def perform_create(
            self,
            serializer: RegistrationSerializer,
            **kwargs: None,
    ) -> None:
        """Perform the task of sending a message about the user creation."""
        with transaction.atomic():
            user = serializer.save(**kwargs)
            context = get_context(user, self.request, app_settings.EMAIL_HOST_USER)
            registration = users_services.UserRegistrationService(user, context)
            registration.execute()

    @action(methods=['POST'], detail=False)
    def registration(
            self, request: Request, *args: None, **kwargs: None
    ):
        """User registration method."""
        return self.create(request, *args, **kwargs)

    #
    # @action(methods=['POST'], detail=False)
    # def activation(self, request: Request, *args: None, **kwargs: None) -> Response:
    #     """Method for activating user"""
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.user
    #     context = get_context(user, request, settings.SEND_CONFIRMATION_EMAIL)
    #     activation = users_services.UserActivationService(user, context)
    #     activation.execute()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def change_password(self, request: Request) -> Response:
        """Method for changing the password."""
        user = get_current_user()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def reset_password(
            self, request: Request, *args: None, **kwargs: None
    ) -> Response:
        """Method for requesting a new password via email."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_current_user()
        context = get_context(user, request, bool(user))
        reset_password = users_services.UserResetPasswordService(user, context)
        reset_password.execute()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def reset_password_confirm(
            self, request: Request, *args: None, **kwargs: None
    ) -> Response:
        """Method for password reset."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        context = get_context(
            user=user,
            request=request,
            send_email=settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION,
        )
        reset_password_confirm = users_services.UserResetPasswordConfirmService(
            user=user, serializer=serializer, context=context
        )
        reset_password_confirm.execute()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def me(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Method for viewing the user."""
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['PUT', 'PATCH'], detail=False)
    def edit(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Method for editing the user."""
        dict_methods = {'PUT': self.update, 'PATCH': self.partial_update}
        for method, func in dict_methods.items():
            if request.method == method:
                return func(*args, **kwargs)

    @action(methods=['PATCH'], detail=True)
    def edit_role(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Method for editing a user's role."""
        return self.partial_update(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        filters=True,
        summary='Search through the user list',
        tags=['Search'],
    )
)
class UserListSearchView(mixins.ListViewSet):
    """User list view."""
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = user_s.UserListSearchSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('email', 'username')
    ordering = ('username', '-id')
