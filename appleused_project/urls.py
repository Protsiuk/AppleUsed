from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from accounts.views import main_page
from django.views.generic.base import TemplateView

# from rest_framework.documentation import include_docs_urls
#
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', main_page, name='main'),

    url(r'accounts/', include('accounts.urls')),
    url(r'advertisements/', include('advertisements.urls')),

    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'registrations/accounts/', include('registration.backends.hmac.urls')),

    # url(r'password_reset/', include('password_reset.urls')),

    # url(r'home')?, home_pages, name='home'
    # url(r'send_email/', include('send_email.urls')),
    # url('', TemplateView.as_view(template_name='main.html'), name='home'),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
if settings.DEBUG:
    # urlpatterns += staticfiles_urlpatterns()
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)