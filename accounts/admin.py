from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import WebsiteSettings, MyCustomUser
from accounts.forms import EditProfileUserForm, MyCustomUserCreationForm
from solo.admin import SingletonModelAdmin


@admin.register(MyCustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = EditProfileUserForm
    form = MyCustomUserCreationForm

    list_display = ([field.name for field in MyCustomUser._meta.fields])

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_moderator', 'date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'location_user', 'phone_number_user', 'birth_day')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_moderator', 'is_superuser')}),
        (_('Important data'), {'fields': ('last_login', 'date_joined')}),)

admin.site.register(WebsiteSettings, SingletonModelAdmin)
