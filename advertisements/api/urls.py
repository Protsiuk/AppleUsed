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
    # url(r'^advertisement/(?P<pk>[\d]+)/$', AdDetailAPIView.as_view(), name='ad-api-detail'),
    url(r'^advertisements/$', AdsListAPIView.as_view(), name='ads-list-api'),
    # url(r'^advertisement/create/$', CreateAdApiView.as_view(), name='ads-create-api'),
    # url(r'^api/v1.0/advertisements/$', AdvListAPIView.as_view(), name='ad-api-detail'),
]
