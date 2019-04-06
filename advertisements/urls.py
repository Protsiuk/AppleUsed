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
    # AdvertisementMessageView,
    AjaxAPIAdmarkView,
    )
    # GetSingleAdvertisementView, CreateAdvertisementView #publications_as_json,

# app_name = 'advertisement'
urlpatterns = [

    #---URL for API------
    url(r'^api/(?P<pk>[\d]+)/favorite$', AjaxAPIAdmarkView.as_view(), name='ad-api-favorite'),

    # -----------CBV---------
    url(r'^(?P<pk>[\d]+)$', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    url(r'^create/', AdvertisementCreateView.as_view(), name='new_advertisement'),
    url(r'^(?P<pk>[\d]+)/edit/', AdvertisementUpdateView.as_view(), name='edit_ad'),
    url(r'^(?P<pk>[\d]+)/delete/', AdvertisementDeleteView.as_view(), name='delete_ad'),

    # url(r'^(?P<pk>[\d]+)$', AdvertisementMarkMixinView.as_view(), name='advertisement_detail'),
    url(r'^search-list/', AdvertisementsSearchView.as_view(), name='search_list'),
    url(r'^favorites/$', AdvertisementsListMarksView.as_view(), name='favorites'),
    url(r'my_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_advertisements'),
    url(r'my_active_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_active_advertisements'),
    url(r'my_archive_advertisements/$', MyAdvertisementArchiveView.as_view(), name='archive_advertisements'),

    url(r'^$', AdvertisementHomeView.as_view(), name='main'),


    # url(r'^(?P<pk>[\d]+)$', AdvertisementMessageView.as_view(), name='advertisement_detail'),
    # url(r'^(?P<advertisement_id>[\d]+)/(?P<slug>[-\w]+)/$', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    # url(r'^(?P<advertisement_id>[\d]+)/like$', like_single_publication, name='like_single_publication'),
    # url(r'^api/(?P<publication_id>[\d]+)$', publications_as_json),
    # url(r'^api/(?P<advertisement_id>[\d]+)$', GetSingleAdvertisementView.as_view()),
    # url(r'^api/create', CreateAdvertisementView.as_view()),
]