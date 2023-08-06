from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from demo.settings import DEBUG, MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

if DEBUG:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}), )
