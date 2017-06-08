"""Urls of advertisements in project "appleused_project"
"""

from django.conf.urls import url
from advertisements.views import advertisements, single_advertisement #, new_advertisement # like_single_publication, \
    # GetSingleAdvertisementView, CreateAdvertisementView #publications_as_json,

urlpatterns = [

    url(r'^$', advertisements, name='advertisements'),
    url(r'^(?P<advertisement_id>[\d]+)$', single_advertisement, name='single_advertisement'),
    # url(r'^(?P<advertisement_id>[\d]+)$', new_advertisement, name='new_advertisement'),

    # url(r'^(?P<advertisement_id>[\d]+)/like$', like_single_publication, name='like_single_publication'),
    # url(r'^api/(?P<publication_id>[\d]+)$', publications_as_json),
    # url(r'^api/(?P<advertisement_id>[\d]+)$', GetSingleAdvertisementView.as_view()),
    # url(r'^api/create', CreateAdvertisementView.as_view()),
]