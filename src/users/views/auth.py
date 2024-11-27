from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response
from rest_framework_simplejwt import views

from users.jwt.tokens import add_tokens_to_response


@extend_schema_view(
    post=extend_schema(
        summary='Создание токена',
        tags=['Аутентификация'],
    ),
)
class CustomTokenObtainPairView(views.TokenObtainPairView):
    """Представление для создания токена."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data
        access_token = tokens.get('access')
        refresh_token = tokens.get('refresh')

        custom_response = Response("Вход выполнен успешно")
        add_tokens_to_response(custom_response, access_token, refresh_token)
        return custom_response


@extend_schema_view(
    post=extend_schema(
        summary='Обновление токена',
        tags=['Аутентификация'],
    ),
)
class CustomTokenRefreshView(views.TokenRefreshView):
    """Представление для обновления токена."""
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Проверка токена',
        tags=['Аутентификация'],
    ),
)
class CustomTokenVerifyView(views.TokenVerifyView):
    """Представление проверки токена."""
    pass
