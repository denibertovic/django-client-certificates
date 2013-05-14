from uuid import uuid4

from django.db import models
from django.conf import settings


class Cert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    x509 = models.TextField(blank=True)
    pub_key = models.TextField(blank=True)

    uuid = models.CharField(max_length=255, default=lambda: uuid4().get_hex(),
            unique=True)
    description = models.TextField(blank=True)

    country = models.CharField(max_length=2, help_text='ISO3166 2 letter code')
    state = models.CharField(max_length=64)
    locality = models.CharField(max_length=64)
    organization = models.CharField(max_length=64)
    organizational_unit = models.CharField(max_length=64)
    common_name = models.CharField(max_length=64)

    is_valid = models.BooleanField(default=True)
    valid_until = models.DateTimeField()

    is_installed = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return ('certs_install_certificate', (), {'uuid': self.uuid})
