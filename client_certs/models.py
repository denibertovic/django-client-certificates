from django.db import models
from django.conf import settings

from .cert import create_self_signed_client_cert


class Cert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    x509 = models.TextField()
    export_password = models.CharField(max_length=255)

    country = models.CharField(max_length=2, help_text='ISO3166 2 letter code')
    state = models.CharField(max_length=64)
    locality = models.CharField(max_length=64)
    organization = models.CharField(max_length=64)
    organizational_unit = models.CharField(max_length=64)
    common_name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.x509 = create_self_signed_client_cert(
            country=self.country,
            state=self.state,
            locality=self.locality,
            organization=self.organization,
            organizational_unit=self.organizational_unit,
            common_name=self.common_name,
            email=self.user.email)
        print self.x509
        super(Cert, self).save(*args, **kwargs)
