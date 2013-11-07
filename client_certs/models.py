from uuid import uuid4

from OpenSSL import crypto

from django.db import models
from django.conf import settings

from .cert import create_signed_client_cert


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

    def generate_and_sign_client_cert(self, pub_key):

        spki = crypto.NetscapeSPKI(pub_key)
        self.pub_key = pub_key

        x509 = create_signed_client_cert(
            client_public_key=spki.get_pubkey(),
            country=self.country,
            state=self.state,
            locality=self.locality,
            organization=self.organization,
            organizational_unit=self.organizational_unit,
            common_name=self.common_name,
            email=self.user.email,
            valid_until=self.valid_until)

        self.x509 = crypto.dump_certificate(crypto.FILETYPE_PEM, x509)
        self.is_installed = True
        self.save()

        return x509
