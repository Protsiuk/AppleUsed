from django.contrib import admin
from advertisements.models import Advertisement, AdvertisementImage, AdvertisementFollowing, AdvertisementMessage, SiteConfiguration
# from advertisements.forms import AdvertisementForm

# Register your models here.
# admin.site.register(SiteConfiguration)
# admin.site.register(Advertisement)
admin.site.register(AdvertisementImage)
admin.site.register(AdvertisementFollowing)
admin.site.register(AdvertisementMessage)


# class ChoiceInline(admin.StackedInline):
#     model = Advertisement
#     extra = 3
#
# class AdvertisementAdmin(admin.ModelAdmin):
#     inlines = [ChoiceInline]
#
# admin.site.register(Advertisement, AdvertisementAdmin)

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    # add_form = UpdateAdvertisementForm
    # form = MyCustomUserCreationForm
    # form = AdvertisementForm

    list_display = [
        'id',
        'title',
        'category_equipment',
        'price',
        'phone_author',
        'description',
        'location_author',
        'author',
        'product_number'
        ]
    exclude = ('phone_regex',)
    list_filter = ['author', 'title', 'is_active', 'created']
#     # fieldsets = (
#     #     (None, {'fields': ('email', 'username', 'password')}),
    #     (_('Personal info'), {'fields': ('first_name', 'last_name', 'locations_user', 'phone_number_user', 'birth_day')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    #     (_('Important data'), {'fields': ('last_login', 'date_joined')}),
    # )
    ordering = ['-created']
#     # ordering = ["email"]

