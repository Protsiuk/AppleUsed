"""Urls of moderation in project "AppleUsed"
"""

from django.conf.urls import url
from moderation.views import (
    ListForModerateView,
    ModerationDetailView,
    ModerationFinishedView,
    ModerationBeginView,
    MyListModerationView,
    )

app_name = 'moderation'

urlpatterns = [

    # -----------CBV---------

    url(r'^$', ListForModerateView.as_view(), name='list_for_moderation'),
    url(r'^(?P<pk>[\d]+)/archive/$', ModerationDetailView.as_view(), name='moderate_detail_archive'),
    url(r'^moderate/(?P<pk>[\d]+)/start/$', ModerationBeginView.as_view(), name='moderate_begin'),
    url(r'^moderate/(?P<pk>[\d]+)$', ModerationFinishedView.as_view(), name='moderate_ad'),
    url(r'^my_list_moderation/$', MyListModerationView.as_view(), name='my_list_moderation'),
]
