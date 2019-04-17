from django.contrib import admin
from moderation.models import Checklist, Moderation


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


# @admin.register(Moderator)
# class ModeratorAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Moderator._meta.fields]
#     list_filter = [field.name for field in Moderator._meta.fields]
#     ordering = ['-appointment']
#
#     class Meta:
#         model = Moderator


@admin.register(Moderation)
class ModerationAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = [field.name for field in Moderation._meta.fields]
    list_filter = [field.name for field in Moderation._meta.fields]
    # fieldsets = (
    # )
    # list_filter = ['author', 'title', 'price', 'is_active', 'created', 'updated', 'phone_author']
    ordering = ['-end_moderate']

    class Meta:
        model = Moderation


# Register your models here.
# admin.site.register(Moderation)
# admin.site.register(Moderator)

# admin.site.register(AdvertisementImage, AdvertisementImageAdmin)
