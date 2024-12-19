from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from rest_framework.request import Request

User = get_user_model()


# TODO: To make this work, uncomment in settings.py MIDDLEWARE at the end of the project.

class ActiveUserMiddleware(MiddlewareMixin):
    """Class for implementing the functionality of customer status: Online/Offline."""

    @staticmethod
    def process_request(request: Request) -> None:
        """
        Checks if the user is authenticated and whether their session has a unique session_key.
        """
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f'last-seen-{request.user.id}'
            last_login = cache.get(cache_key)

            if not last_login:
                User.objects.filter(pk=request.user.id).update(
                    last_login=timezone.now()
                )
                # Set cache for 300 seconds with the current timestamp
                # using the key last-seen-id-user.
                cache.set(cache_key, timezone.now(), 300)
