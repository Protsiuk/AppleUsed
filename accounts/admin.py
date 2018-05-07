from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import User, WebsiteSettings

from solo.admin import SingletonModelAdmin


class CustomUserAdmin(UserAdmin):
    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}
                      ),
                     )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important data'), {'fields': ('last_login', 'date_joined')}),
    )

    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    #     (_('Important data'), {'fields': ('last_login', 'date_joined')}),
    # )
    list_filter = ('is_staff', 'is_superuser', 'is_active')


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(WebsiteSettings, SingletonModelAdmin)

# ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
