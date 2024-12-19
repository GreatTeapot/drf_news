from typing import Union

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe, SafeString
from django.utils.translation import gettext_lazy as _

from .models.profile import Profile
from .models.users import User


# region ----------------------------- INLINE ---------------------------------------
class ProfileAdmin(admin.TabularInline):
    """
    Embedded profile model for UserAdmin.
    
    Attributes:
        * `model` (Profile): the profile model.
        * `fields` (tuple[str]): fields.
        * `readonly_fields` (tuple[str]): read-only fields.
    """

    model = Profile
    fields = ('photo', 'photo_show')
    readonly_fields = ('photo_show',)

    @admin.display(description='Photo', ordering='photo')
    def photo_show(self, obj: Profile) -> Union[SafeString, str]:
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='60' />")
        return 'No photo'


# endregion -------------------------------------------------------------------------


# region -------------------------- MODEL ADMIN -------------------------------------
@admin.register(User)
class UserAdmin(UserAdmin):
    """
    User admin model.
    
    Attributes:
        * `change_user_password_template` (None): change user password template.
        * `fieldsets` (tuple[tuple[...]]): field groups.
        * `add_fieldsets` (tuple[tuple[...]]): add field groups.
        * `list_display` (tuple[str]): list display.
        * `list_filter` (tuple[str]): list filter.
        * `search_fields` (tuple[str]): search fields.
        * `filter_horizontal` (tuple[str]): horizontal filter.
        * `readonly_fields` (tuple[str]): read-only fields.
        * `inlines` (tuple[ProfileAdmin]): inlines.
    """
    # region -------------- АТРИБУТЫ МОДЕЛИ АДМИНА ПОЛЬЗОВАТЕЛЯ ---------------------
    change_user_password_template = None
    fieldsets = (
        (None,
         {'fields': ('phone_number', 'email', 'username')}),
        (_('Personal information'),
         {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active',  'is_superuser',
                       'groups', 'user_permissions',)
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'full_name', 'email', 'phone_number',)

    list_display_links = ('id', 'full_name',)
    list_filter = ('is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'id', 'email', 'phone_number',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)

    inlines = (ProfileAdmin,)
    # endregion ---------------------------------------------------------------------
# endregion -------------------------------------------------------------------------
