from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

#
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'accounts/', include('accounts.urls')),
    url(r'advertisements/', include('advertisements.urls')),
    url(r'moderation/', include('moderation.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^chat/', include('chat.urls')),

    url(r'^$', RedirectView.as_view(permanent = False, url = '/advertisements/'), name='go_to_main'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

