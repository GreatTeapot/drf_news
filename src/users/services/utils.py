from __future__ import annotations
from typing import TYPE_CHECKING, Union, Optional

if TYPE_CHECKING:
    from django.urls import URLPattern
    from rest_framework.request import Request
    from ..models.users import User


def is_route_selected(url_pattern: URLPattern) -> bool:
    """
    Check for the selected endpoint.
    If there are points that are in the unauthorized list (unauthorised_urls),
    they will not appear in the schema.
    """
    unauthorised_urls = (
        '',
        'resend_activation/',
        'reset_username/',
        'reset_username_confirm/',
        'set_password/',
        'set_username/',
    )
    for url in unauthorised_urls:
        match = url_pattern.resolve(url)
        if match:
            return False
    return True


def get_context(
        user: User, request: Request, send_email: bool
) -> Optional[dict[str, Union[str, int]]]:
    """Get the context for sending an email."""
    if send_email:
        context = {
            'user_id': user.pk,
            'domain': request.get_host(),
            'protocol': 'https' if request.is_secure() else 'http',
            'site_name': request.get_host(),
        }
        return context
