from django.contrib import admin
from advertisements.models import Advertisement, AdvertisementImage, AdvertisementFollowing, PageHit, SiteConfiguration


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
    list_filter = ['id', 'advertisement', 'date', 'hits_counter']
    ordering = ['-date']

    class Meta:
        model = PageHit


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_per_page = 15
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
        'is_moderated',
        'slug',
        'product_number',
        'created',
        'updated',
        ]
    list_filter = ['author', 'title', 'price', 'is_active', 'is_moderated', 'created', 'updated', 'phone_author']
    inlines = [AdvertisementImageInline]
    ordering = ['-created']

    class Meta:
        model = Advertisement


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

    class Meta:
        model = AdvertisementImage



admin.site.register(SiteConfiguration)
# admin.site.register(AdvertisementMessage)
admin.site.register(AdvertisementImage, AdvertisementImageAdmin)
