from datetime import datetime, timedelta
from typing import Tuple

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

def generate_tokens(user) -> Tuple[str, str]:
    """Generating tokens"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)

def add_tokens_to_response(response: Response, access_token: str, refresh_token: str) -> Response:
    """Adding tokens to cookies """

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False,  # Установить в True на HTTPS
        samesite='Lax',
        

    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='Lax',

    )
    return response
