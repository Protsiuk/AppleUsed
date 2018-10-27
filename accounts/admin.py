from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import MyCustomUser, WebsiteSettings

from solo.admin import SingletonModelAdmin


@admin.register(MyCustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_number_user', 'date_joined', 'locations_user']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important data'), {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ["email"]

# class CustomUserAdmin(UserAdmin):
#     add_fieldsets = ((None, {
#         'classes': ('wide',),
#         'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}
#                       ),
#                      )
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#         (_('Important data'), {'fields': ('last_login', 'date_joined')}),
#     )
#     list_filter = ('is_staff', 'is_superuser', 'is_active')
# -------------
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    #     (_('Important data'), {'fields': ('last_login', 'date_joined')}),
    # )


# Register your models here.
# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(WebsiteSettings, SingletonModelAdmin)

# ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
