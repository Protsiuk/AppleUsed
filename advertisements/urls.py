"""Urls of advertisements in project "appleused_project"
"""

from django.conf.urls import url
# from advertisements.views import advertisements, single_advertisement, ordering_list, new_advertisement # like_single_publication, \
from advertisements.views import AdvertisementCreateView, AdvertisementHomeView, AdvertisementDetailView, \
    AdvertisementsSearchView, AdvertisementMarkMixinView, AdvertisementsListMarksView, MyAdvertisementActiveView, \
    MyAdvertisementArchiveView, AdvertisementUpdateView, AdvertisementMessageView
    # GetSingleAdvertisementView, CreateAdvertisementView #publications_as_json,

urlpatterns = [

    # -----------CBV---------

    url(r'^create/', AdvertisementCreateView.as_view(), name='new_advertisement'),
    url(r'^(?P<pk>[\d]+)/edit/', AdvertisementUpdateView.as_view(), name='edit_ad'),
    # url(r'^(?P<advertisement_id>[\d]+)$', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    url(r'^(?P<pk>[\d]+)$', AdvertisementDetailView.as_view(), name='advertisement_detail'),
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