"""Urls of Chats in project "AppleUsed"
"""

from django.conf.urls import url
from chat.views import (
    DialogsListView,
    CurrentDialogView,
    DeleteDialogView,
    )

app_name = 'chat'
urlpatterns = [
    # -----------CBV---------
    url(r'^$', DialogsListView.as_view(), name='dialog_list'),
    url(r'^(?P<pk>[\d]+)/current-dialog/$', CurrentDialogView.as_view(), name='current_dialog'),
    url(r'^(?P<pk>[\d]+)/dialog-delete/$', DeleteDialogView.as_view(), name='dialog-delete'),
]
