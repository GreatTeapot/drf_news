
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import views

from users.jwt.tokens import add_tokens_to_response


@extend_schema_view(
    post=extend_schema(
        summary='Token creation',
        tags=['Аутентификация'],
    ),
)
class CustomTokenObtainPairView(views.TokenObtainPairView):
    """View for creating a token."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data
        access_token = tokens.get('access')
        refresh_token = tokens.get('refresh')

        custom_response = Response("Login Successful")
        add_tokens_to_response(custom_response, access_token, refresh_token)
        return custom_response


@extend_schema_view(
    post=extend_schema(
        summary='Token refresh',
        tags=['Аутентификация'],
    ),
)
class CustomTokenRefreshView(views.TokenRefreshView):
    """View for refreshing a token."""
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Token verification',
        tags=['Аутентификация'],
    ),
)
class CustomTokenVerifyView(views.TokenVerifyView):
    """View for verifying a token."""
    pass
