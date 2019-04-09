from django.contrib import admin
from moderation.models import Checklist, Moderator, Moderation


# class ChoiceInline(admin.StackedInline):
#     model = Advertisement
#     extra = 3
#
# class AdvertisementAdmin(admin.ModelAdmin):
#     inlines = [ChoiceInline]
#
# admin.site.register(Advertisement, AdvertisementAdmin)
#
# # class AdvertisementImageInline(admin.TabularInline):
# class AdvertisementImageInline(admin.StackedInline):
#     model = AdvertisementImage


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'check_title',
        'check_description',
        'check_photos',
        ]
    list_filter = ['id', 'check_title', 'check_description']
    exclude = ()

    class Meta:
        model = Checklist


@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    # list_display = [
    #     'id',
    #     'advertisement',
    #     'advertisement_id',
    #     'date',
    #     'hits_counter',
    #     ]
    list_display = [field.name for field in Moderator._meta.fields]
    # exclude = ()
    list_filter = [field.name for field in Moderator._meta.fields]
    ordering = ['-appointment']

    class Meta:
        model = Moderator


@admin.register(Moderation)
class ModerationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Moderation._meta.fields]

    # list_display = [
    #     'id',
    #     'title',
    #     'description',
    #     'category_equipment',
    #     'price',
    #     'author',
    #     'phone_author',
    #     'location_author',
    #     'main_image',
    #     'is_active',
    #     'slug',
    #     'product_number',
    #     'created',
    #     'updated',
    #     # 'hit_counter',
    #     ]
    # exclude = ('phone_regex',)
    list_filter = [field.name for field in Moderation._meta.fields]
    # list_filter = ['author', 'title', 'price', 'is_active', 'created', 'updated', 'phone_author']
    ordering = ['-end_moderate']

    class Meta:
        model = Moderation




# Register your models here.
# admin.site.register(Moderation)
# admin.site.register(Moderator)

# admin.site.register(AdvertisementImage, AdvertisementImageAdmin)
