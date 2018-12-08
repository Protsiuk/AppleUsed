from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import WebsiteSettings, MyCustomUser
from accounts.forms import EditProfileUserForm, MyCustomUserCreationForm#, CustomUserChangeForm

from solo.admin import SingletonModelAdmin


@admin.register(MyCustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = EditProfileUserForm
    # form = MyCustomUserCreationForm
    form = EditProfileUserForm

    list_display = [
        'id', 'email', 'first_name', 'last_name', 'phone_number_user', 'locations_user', 'date_joined', 'birth_day'
        ]
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'locations_user', 'phone_number_user', 'birth_day')}),
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
# admin.site.register(MyCustomUser, UserAdmin)
admin.site.register(WebsiteSettings, SingletonModelAdmin)

# ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
