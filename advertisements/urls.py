"""Urls of advertisements in project "appleused_project"
"""

from django.conf.urls import url
from advertisements.views import (
    AdvertisementCreateView,
    AdvertisementHomeView,
    AdvertisementDetailView,
    AdvertisementsSearchView,
    AdvertisementsListMarksView,
    MyAdvertisementActiveView,
    MyAdvertisementArchiveView,
    AdvertisementUpdateView,
    AdvertisementDeleteView,
    AdvertisementDeactivateView,
    AjaxAPIAdmarkView,
    )

# app_name = 'advertisement'
urlpatterns = [

    #---URL for API------
    url(r'^api/(?P<pk>[\d]+)/favorite$', AjaxAPIAdmarkView.as_view(), name='ad-api-favorite'),

    # -----------CBV---------
    url(r'^(?P<pk>[\d]+)$', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    url(r'^create/', AdvertisementCreateView.as_view(), name='new_advertisement'),
    url(r'^(?P<pk>[\d]+)/edit/', AdvertisementUpdateView.as_view(), name='edit_ad'),
    url(r'^(?P<pk>[\d]+)/deactivate/', AdvertisementDeactivateView.as_view(), name='deactivate_ad'),
    url(r'^(?P<pk>[\d]+)/delete/', AdvertisementDeleteView.as_view(), name='delete_ad'),
    url(r'^search-list/', AdvertisementsSearchView.as_view(), name='search_list'),
    url(r'^favorites/$', AdvertisementsListMarksView.as_view(), name='favorites'),
    url(r'my_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_advertisements'),
    url(r'my_active_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_active_advertisements'),
    url(r'my_archive_advertisements/$', MyAdvertisementArchiveView.as_view(), name='archive_advertisements'),
    url(r'^$', AdvertisementHomeView.as_view(), name='main'),
]
