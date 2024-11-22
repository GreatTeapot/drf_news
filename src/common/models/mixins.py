from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .base import BaseModel

User = get_user_model()


class DateMixin(BaseModel):
    """
    Abstract date and time model.

    Attributes:
        * `created_at` (DateTimeField): created at
        * `updated_at` (DateTimeField): updated at
    """

    created_at = models.DateTimeField(
        verbose_name='Created at',
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Updated at',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """Save creation and update timestamps."""

        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DateMixin, self).save(*args, **kwargs)


class InfoMixin(DateMixin):
    """
    Abstract information model.

    Attributes:
        * `created_by` (ForeignKey): created by
        * `updated_by` (ForeignKey): updated by
    """

    created_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='created_%(app_label)s_%(class)s',
        verbose_name='Created by',
        null=True,
    )
    updated_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='updated_%(app_label)s_%(class)s',
        verbose_name='Updated by',
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """Save creation and update information."""

        user = get_current_user()

        if user and not user.pk:
            user = None

        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)
