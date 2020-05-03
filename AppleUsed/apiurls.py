from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

#
urlpatterns = [
    url(r'accounts/', include('accounts.api.urls')),
    url(r'ads/', include('advertisements.api.urls', namespace='api-ads')),

    url(r'^$', RedirectView.as_view(permanent=False, url='/advertisements/'), name='go_to_main'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

