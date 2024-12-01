from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import IsAuthenticated

if TYPE_CHECKING:
    from rest_framework.request import Request
    from news.views.news import NewsViewSet

class IsAuthor(IsAuthenticated):
    """Permission class to check if the user is the author based on their role"""

    message = (
        'You do not have permission to perform this action'
    )

    def has_permission(self, request: Request, view: NewsViewSet) -> bool:
        if request.user.Role.AUTHOR:
            return True
        return False


