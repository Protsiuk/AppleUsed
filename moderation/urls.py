"""Urls of moderation in project "appleused_project"
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

    #---URL for API------
    # url(r'^api/(?P<pk>[\d]+)/favorite$', AjaxAPIAdmarkView.as_view(), name='ad-api-favorite'),

    # -----------CBV---------

    url(r'^$', ListForModerateView.as_view(), name='list_for_moderation'),
    url(r'^(?P<pk>[\d]+)/archive/$', ModerationDetailView.as_view(), name='moderate_detail_archive'),
    url(r'^moderate/(?P<pk>[\d]+)/start/$', ModerationBeginView.as_view(), name='moderate_begin'),
    url(r'^moderate/(?P<pk>[\d]+)$', ModerationFinishedView.as_view(), name='moderate_detail'),
    url(r'^my_list_moderation/$', MyListModerationView.as_view(), name='my_list_moderation'),

    # url(r'^(?P<pk>[\d]+)$', ModerationDetailView.as_view(), name='moderation_detail'),

    # url(r'^favorites/$', AdvertisementsListMarksView.as_view(), name='favorites'),
    # url(r'my_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_advertisements'),
    # url(r'my_active_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_active_advertisements'),
    # url(r'my_archive_advertisements/$', MyAdvertisementArchiveView.as_view(), name='archive_advertisements'),

    # url(r'^$', AdvertisementHomeView.as_view(), name='main'),

]