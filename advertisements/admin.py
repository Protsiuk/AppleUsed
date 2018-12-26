from django.contrib import admin
from advertisements.models import Advertisement, AdvertisementImage, AdvertisementFollowing, AdvertisementMessage, SiteConfiguration
# from advertisements.forms import AdvertisementForm


# class ChoiceInline(admin.StackedInline):
#     model = Advertisement
#     extra = 3
#
# class AdvertisementAdmin(admin.ModelAdmin):
#     inlines = [ChoiceInline]
#
# admin.site.register(Advertisement, AdvertisementAdmin)

# class AdvertisementImageInline(admin.TabularInline):
class AdvertisementImageInline(admin.StackedInline):
    model = AdvertisementImage


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    # add_form = UpdateAdvertisementForm
    # form = AdvertisementForm
    list_display = [
        'id',
        'title',
        'slug',
        'category_equipment',
        'price',
        'phone_author',
        'description',
        'location_author',
        'author',
        'product_number',
        'created',
        'updated',
        ]
    # exclude = ('phone_regex',)
    list_filter = ['author', 'title', 'is_active', 'created']
    inlines = [AdvertisementImageInline]
#     # fieldsets = (
#     #     (None, {'fields': ('email', 'username', 'password')}),
    #     (_('Personal info'), {'fields': ('first_name', 'last_name', 'locations_user', 'phone_number_user', 'birth_day')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    #     (_('Important data'), {'fields': ('last_login', 'date_joined')}),
    # )
    ordering = ['-created']
#     # ordering = ["email"]

    class Meta:
        model = Advertisement


# @admin.register(AdvertisementImage)
class AdvertisementImageAdmin(admin.ModelAdmin):
    # add_form = UpdateAdvertisementForm
    # form = AdvertisementForm
    list_display = [
        'id',
        'advertisement',
        'image',
        'main_image',
        'created',
        'updated',
        'is_active',
        ]
    # exclude = ('phone_regex',)
    list_filter = ['advertisement', 'created', 'updated', 'is_active']
    # inlines = [AdvertisementImageInline]

    class Meta:
        model = AdvertisementImage


# Register your models here.
# admin.site.register(SiteConfiguration)
# admin.site.register(Advertisement)
# admin.site.register(AdvertisementImage)
admin.site.register(AdvertisementFollowing)
admin.site.register(AdvertisementMessage)
admin.site.register(AdvertisementImage, AdvertisementImageAdmin)
