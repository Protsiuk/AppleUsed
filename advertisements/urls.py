"""Urls of advertisements in project "appleused_project"
"""

from django.conf.urls import url
from advertisements.views import advertisements, single_advertisement, filter_list, create_advertisement#\
    # ordering_list, GetSingleAdvertisementView, CreateAdvertisementView #publications_as_json,

urlpatterns = [

    url(r'^$', advertisements, name='advertisements'),
    url(r'^Home$', advertisements, name='Home'),

    # url(r'^order_price_expensive/', ordering_list, name='advertisements_sorted_expensive'),
    # url(r'^order_price_inexpensive/', advertisements, name='advertisements_sorted_inexpensive'),

    # url(r'^order_price_down/', advertisements_order_price_down, name='advertisements_price_down'),
    # # url(r'^order_price_up/', advertisements_order_price_up, name='advertisements_price_up'),
    # url(r'^find_(?P<title>)/', advertisements_order_price_down, name='advertisements_price_down'),

    # url(r'^(?P<advertisement_id>[\d]+)$', single_advertisement, name='single_advertisement'),# Антон показував
    url(r'^(?P<advertisement_id>\d+)/$', single_advertisement, name='single_advertisement'),

    url(r'^create_advertisement', create_advertisement, name='create_advertisement'),
    url(r'^send_advertisement_success', create_advertisement, name='send_advertisement_success'),


    # url(r'^(?P<advertisement_id>[\d]+)/like$', like_single_publication, name='like_single_publication'),
    # url(r'^api/(?P<publication_id>[\d]+)$', publications_as_json),
    # url(r'^api/(?P<advertisement_id>[\d]+)$', GetSingleAdvertisementView.as_view()),
    # url(r'^api/create', CreateAdvertisementView.as_view()),
]