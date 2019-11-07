from django.contrib import admin
from moderation.models import Checklist, Moderation

# @admin.register(Checklist)
# class ChecklistAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'check_title',
#         'check_description',
#         'check_photos',
#         ]
#     list_filter = ['id', 'check_title', 'check_description']
#     exclude = ()
#
#     class Meta:
#         model = Checklist


@admin.register(Moderation)
class ModerationAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = [field.name for field in Moderation._meta.fields]
    list_filter = [field.name for field in Moderation._meta.fields]
    ordering = ['-end_moderate']

    class Meta:
        model = Moderation
