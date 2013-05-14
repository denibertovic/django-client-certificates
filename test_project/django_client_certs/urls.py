from django.conf.urls import patterns, include, url

from client_certs import urls as client_cert_urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index'),
    url(r'^certs/', include(client_cert_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
