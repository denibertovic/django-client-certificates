from django.conf.urls import patterns, include, url
from django.conf import settings

from client_certs import urls as client_cert_urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index'),
    url(r'^certs/', include(client_cert_urls)),
    url(r'^admin/', include(admin.site.urls)),
)


## STATIC AND MEDIA
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )
