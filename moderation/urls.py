"""Urls of moderation in project "appleused_project"
"""

from django.conf.urls import url
from moderation.views import (
    ListForModerateView,
    # ModerateDetailView,
    ModerationFinishedView,
    ModerationBeginView,
    # TestStartview,
    )

app_name = 'moderation'
urlpatterns = [

    #---URL for API------
    # url(r'^api/(?P<pk>[\d]+)/favorite$', AjaxAPIAdmarkView.as_view(), name='ad-api-favorite'),

    # -----------CBV---------
    # url(r'^(?P<pk>[\d]+)$', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    # url(r'^create/', AdvertisementCreateView.as_view(), name='new_advertisement'),
    # url(r'^(?P<pk>[\d]+)/edit/', AdvertisementUpdateView.as_view(), name='edit_ad'),
    # url(r'^(?P<pk>[\d]+)/delete/', AdvertisementDeleteView.as_view(), name='delete_ad'),

    # url(r'^(?P<pk>[\d]+)$', AdvertisementMarkMixinView.as_view(), name='advertisement_detail'),

    url(r'^$', ListForModerateView.as_view(), name='list_for_moderation'),
    # url(r'^(?P<pk>[\d]+)$', ModerationStartView.as_view(), name='moderate_detail'),
    # url(r'^moderate/(?P<pk>[\d]+)$', ModerationBeginView.as_view(), name='moderate_detail'),
    url(r'^moderate/(?P<pk>[\d]+)$', ModerationFinishedView.as_view(), name='moderate_detail'),

    # url(r'^moderate/create/test1', TestStartview.as_view(), name='test_moderation'),

    # url(r'^favorites/$', AdvertisementsListMarksView.as_view(), name='favorites'),
    # url(r'my_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_advertisements'),
    # url(r'my_active_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_active_advertisements'),
    # url(r'my_archive_advertisements/$', MyAdvertisementArchiveView.as_view(), name='archive_advertisements'),

    # url(r'^$', AdvertisementHomeView.as_view(), name='main'),

]