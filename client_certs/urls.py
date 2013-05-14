from django.conf.urls import patterns, url

urlpatterns = patterns(
    'client_certs.views',
    url(r'^install/(?P<uuid>.+)$', 'install_certificate',
        name='certs_install_certificate'))
