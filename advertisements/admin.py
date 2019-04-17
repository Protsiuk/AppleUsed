from django.contrib import admin
from advertisements.models import Advertisement, AdvertisementImage, AdvertisementFollowing, AdvertisementMessage, \
    PageHit, SiteConfiguration

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


@admin.register(AdvertisementFollowing)
class AdvertisementFollowingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'advertisement',
        'get_ad_id',
        'get_author_of_ad',
        'user',
        ]
    list_filter = ['advertisement', 'user']
    # ordering = ['-date']

    class Meta:
        model = AdvertisementFollowing


@admin.register(PageHit)
class PageHitAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'advertisement',
        'advertisement_id',
        'date',
        'hits_counter',
        ]
    # exclude = ('phone_regex',)
    list_filter = ['id', 'advertisement', 'date', 'hits_counter']
    ordering = ['-date']

    class Meta:
        model = PageHit


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_per_page = 15
    # add_form = UpdateAdvertisementForm
    # form = AdvertisementForm
    list_display = [
        'id',
        'title',
        'description',
        'category_equipment',
        'price',
        'author',
        'phone_author',
        'location_author',
        'main_image',
        'is_active',
        'is_visible',
        'slug',
        'product_number',
        'created',
        'updated',
        # 'hit_counter',
        ]
    # exclude = ('phone_regex',)
    list_filter = ['author', 'title', 'price', 'is_active', 'created', 'updated', 'phone_author']
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
    list_display = [
        'id',
        'advertisement',
        'image',
        'created',
        'updated',
        'is_active',
        ]
    list_filter = ['advertisement', 'created', 'updated', 'is_active']
    # inlines = [AdvertisementImageInline]

    class Meta:
        model = AdvertisementImage


# Register your models here.
# admin.site.register(SiteConfiguration)
# admin.site.register(Advertisement)
# admin.site.register(AdvertisementImage)
# admin.site.register(AdvertisementFollowing)
admin.site.register(AdvertisementMessage)
admin.site.register(AdvertisementImage, AdvertisementImageAdmin)
