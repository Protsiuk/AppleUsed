from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from accounts.views import main_page
# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main_page, name='main'),

    url(r'accounts/', include('accounts.urls')),
    url(r'advertisements/', include('advertisements.urls')),

]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
