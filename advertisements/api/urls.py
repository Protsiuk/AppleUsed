"""Urls of advertisements in project "AppleUsed"
"""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from advertisements.api.apiviews import (
    AdDetailAPIView,
    AdsListAPIView,
    CreateAdApiView,
    TestProjectViewSet,
    TestProjectPhotoViewSet,
    AdRetrieveUpdateDeleteAPIView,
    AdvertisementsListMarksViewAPIView,
    MyAdvertisementActiveAPIView,
    MyAdvertisementArchiveAPIView,
    TestUpload
)


# router = DefaultRouter()
# router.register(r'create', CreateAdApiView)
# urlpatterns = router.urls

# router = SimpleRouter()
# router.register(r'test', TestProjectViewSet)
# router.register(r'ads-photo', TestProjectPhotoViewSet)
# urlpatterns = router.urls


app_name = 'advertisement'
urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^test/', TestProjectViewSet.as_view(), name='test'),

    url(r'^advertisement/create/', CreateAdApiView.as_view(), name='test'),
    url(r'^advertisement/(?P<pk>[\d]+)/$', AdRetrieveUpdateDeleteAPIView.as_view(), name='ad-api-detail'),

    url(r'^my_favorite_ads/', AdvertisementsListMarksViewAPIView.as_view(), name='favorites_api'),
    url(r'^my_ads/', MyAdvertisementActiveAPIView.as_view(), name='my_advertisements_api'),
    url(r'my_archive_ads/$', MyAdvertisementArchiveAPIView.as_view(), name='archive_advertisements_api'),

    url(r'^', AdsListAPIView.as_view(), name='ads-list-api'),

    # url(r'^favorites/$', AdvertisementsListMarksView.as_view(), name='favorites'),
    # url(r'my_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_advertisements'),
    # url(r'my_active_advertisements/$', MyAdvertisementActiveView.as_view(), name='my_active_advertisements'),
    # url(r'my_archive_advertisements/$', MyAdvertisementArchiveView.as_view(), name='archive_advertisements'),


    # url(r'^advertisement/(?P<pk>[\d]+)/$', AdDetailAPIView.as_view(), name='ad-api-detail'),
    # url(r'^advertisement/create/$', CreateAdApiView.as_view(), name='ads-create-api'),
    # url(r'^api/v1.0/advertisements/$', AdvListAPIView.as_view(), name='ad-api-detail'),
]
