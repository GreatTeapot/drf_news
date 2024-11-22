from django.core.cache import cache
from django.db import models
from django.utils import timezone

from common.models.base import BaseModel


class Profile(BaseModel):
    """
    User profile model.

    Attributes:
        * `user` (OneToOneField): Linked user.
        * `photo` (ImageField): Profile photo.
    """

    user = models.OneToOneField(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='User',
        primary_key=True,
    )
    photo = models.ImageField(
        verbose_name='Profile Photo',
        upload_to='users/%Y/%m/%d',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self) -> str:
        return f'{self.user} ({self.pk})'

    def is_online(self) -> bool:
        """Check if the user has been online in the last 5 minutes."""
        last_seen = cache.get(f'last-seen-{self.user.id}')
        return bool(last_seen and timezone.now() - last_seen < timezone.timedelta(minutes=5))
