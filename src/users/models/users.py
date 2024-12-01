from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from users.managers.users import CustomUserManager
from users.models.profile import Profile


class User(AbstractUser):
    """
    User model with custom roles.
    """

    class Role(models.TextChoices):
        READER = 'RED', _('Reader')
        ADMIN = 'ADM', _('Administrator')
        AUTHOR = 'AUT', _('Author')

    username = models.CharField(
        verbose_name='Username',
        max_length=32,
        unique=True,
        null=False,
        blank=False,
    )
    role = models.CharField(
        verbose_name='User Role',
        max_length=10,
        choices=Role.choices,
        default=Role.READER,
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        verbose_name='Phone Number',
        unique=True,
        null=True,
        blank=True,
    )
    is_staff = None


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return f'{self.full_name} ({self.pk})'


@receiver(post_save, sender=User)
def post_save_user(sender, instance: User, created, **kwargs) -> None:
    """Create a profile for every new user."""
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
