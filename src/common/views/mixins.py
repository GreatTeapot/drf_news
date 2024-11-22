from typing import Optional, TypeVar

from djoser.views import UserViewSet
from rest_framework import mixins, authentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

TAuth = TypeVar('TAuth')
TPermission = TypeVar('TPermission')
TSerializer = TypeVar('TSerializer')


class ExtendedView:
    """Extended View"""
    authentication_classes = (authentication.BasicAuthentication,)
    multi_authentication_classes = None

    permission_classes = (AllowAny,)
    multi_permission_classes = None

    multi_serializer_class = None
    serializer_class = None

    request = None
    action_map = None

    def __get_action_or_method(self) -> str:
        """Get the action or request method."""
        if hasattr(self, 'action') and self.action:
            return self.action
        return self.request.method

    def __auth_initialize(
            self,
            authentications: Optional[tuple[TAuth]] = None,
    ) -> list[TAuth]:
        """Initialize authentication."""
        auth_classes = (self.authentication_classes if authentications is None
                        else authentications)
        return [auth() for auth in auth_classes]

    def __permission_initialize(
            self,
            permissions: Optional[tuple[TPermission]] = None,
    ) -> list[TPermission]:
        """Initialize permissions."""
        perm_classes = (self.permission_classes if permissions is None
                        else permissions)
        return [permission() for permission in perm_classes]

    def get_authenticators(self) -> list[TAuth]:
        """Get the authenticator classes."""
        assert self.authentication_classes or self.multi_authentication_classes, (
                '"%s" must include either `authentication_classes`, '
                '`multi_authentication_classes`, or override the '
                '`get_authenticators()` method.' % self.__class__.__name__
        )
        if not self.multi_authentication_classes:
            return self.__auth_initialize()

        if self.request is None:
            return self.__auth_initialize()

        # Get the current request method.
        method = self.request.method
        # Find the action associated with the method, if any.
        action = self.action_map.get(method.lower())
        authentications = self.multi_authentication_classes.get(
            action if action else method
        )
        if authentications:
            return self.__auth_initialize(authentications=authentications)
        return self.__auth_initialize()

    def get_permissions(self) -> list[TPermission]:
        """Get the permission classes."""
        assert self.permission_classes or self.multi_permission_classes, (
                '"%s" must include either `permission_classes`, '
                '`multi_permission_classes`, or override the '
                '`get_permissions()` method.' % self.__class__.__name__
        )
        if not self.multi_permission_classes:
            return self.__permission_initialize()

        # Determine the action or request method.
        action = self.__get_action_or_method()
        permissions = self.multi_permission_classes.get(action)
        if permissions:
            return self.__permission_initialize(permissions=permissions)
        return self.__permission_initialize()

    def get_serializer_class(self) -> TSerializer:
        """Get the serializer class."""
        assert self.serializer_class or self.multi_serializer_class, (
                '"%s" must include either `serializer_class`, '
                '`multi_serializer_class`, or override the '
                '`get_serializer_class()` method.' % self.__class__.__name__
        )
        if not self.multi_serializer_class:
            return self.serializer_class

        action = self.__get_action_or_method()
        # Get the serializer for the action or fallback to default.
        return self.multi_serializer_class.get(action) or self.serializer_class


class ExtendedGenericViewSet(ExtendedView, GenericViewSet):
    """Extended Generic ViewSet."""
    pass


class ExtendedUserViewSet(ExtendedView, UserViewSet):
    """Extended User ViewSet."""
    pass


class ExtendedCreateAPIView(ExtendedView, CreateAPIView):
    """Extended Create API View."""
    pass


class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    """View class including List behavior with methods like `get_object`, `get_queryset`, `list`."""
    pass


class CreateViewSet(ExtendedGenericViewSet, mixins.CreateModelMixin):
    """View class including Create behavior."""
    pass


class RetrieveListViewSet(ExtendedGenericViewSet,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin):
    """View class including List and Retrieve behaviors."""
    pass


class CRDListViewSet(ExtendedGenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin):
    """View class including Create, Retrieve, Destroy, and List behaviors."""
    pass


class CUDViewSet(ExtendedGenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    """View class including Create, Update, and Destroy behaviors."""
    pass


class RUDViewSet(ExtendedGenericViewSet,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    """View class including Retrieve, Update, and Destroy behaviors."""
    pass


class CRUListViewSet(ExtendedGenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin):
    """View class including Create, Retrieve, Update, and List behaviors."""
    pass


class CRUDListViewSet(CRUListViewSet,
                      mixins.DestroyModelMixin):
    """View class including full CRUD behaviors."""
    pass
