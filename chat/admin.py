from django.contrib import admin
from chat.models import Message, Chat
# Register your models here.


class MessagesInline(admin.StackedInline):
    model = Message
    list_per_page = 15
    list_display = [field.name for field in Message._meta.fields]
    list_filter = [field.name for field in Message._meta.fields]
    # fieldsets = (
    # )
    # list_filter = ['author', 'title', 'price', 'is_active', 'created', 'updated', 'phone_author']
    ordering = ['-pub_date']

    class Meta:
        model = Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = [field.name for field in Chat._meta.fields]
    list_filter = [field.name for field in Chat._meta.fields]
    inlines = (MessagesInline,)
    search_fields = ['last_send_message']
    # search_fields = ['members', 'last_send_message']

    class Meta:
        model = Chat
