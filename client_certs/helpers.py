import re

from OpenSSL import crypto

from .models import Cert
from .cert import create_signed_client_cert


def create_x509_and_update_cert(user, uuid, pub_key):

    try:
        cert = Cert.objects.get(user=user, uuid=uuid, is_installed=False)
    except Cert.DoesNotExist:
        return None

    regex = re.compile(r'[ \t\n\r\0\x0B]')
    pub_key = regex.sub('', pub_key)

    spki = crypto.NetscapeSPKI(pub_key)
    cert.pub_key = pub_key
    x509 = create_signed_client_cert(
                client_public_key=spki.get_pubkey(),
                country=cert.country,
                state=cert.state, locality=cert.locality,
                organization=cert.organization,
                organizational_unit=cert.organizational_unit,
                common_name=cert.common_name,
                email=cert.user.email,
                valid_until=cert.valid_until)

    cert.x509 = crypto.dump_certificate(crypto.FILETYPE_PEM, x509)
    cert.is_installed = True
    cert.save()

    return x509
