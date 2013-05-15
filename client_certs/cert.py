import logging
from datetime import datetime
import uuid

from django.conf import settings

from OpenSSL import crypto


log = logging.getLogger(__name__)


def create_signed_client_cert(client_public_key, country, state, locality, organization,
        organizational_unit, common_name, email, valid_until):
    """
    Function for generating client certificates
    """

    # load files
    try:
        with open(settings.CERT_CA_FILE) as ca_file:
            ca = crypto.load_certificate(crypto.FILETYPE_PEM, ca_file.read())
        with open(settings.CERT_CA_KEY_FILE) as ca_key_file:
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key_file.read())
    except IOError as e:
        log.error(e)
        raise

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = country
    cert.get_subject().ST = state
    cert.get_subject().L = locality
    cert.get_subject().O = organization
    cert.get_subject().OU = organizational_unit
    cert.get_subject().CN = common_name
    cert.get_subject().emailAddress = email

    cert.set_serial_number(uuid.uuid4().int)

    now = datetime.now()

    cert.set_notBefore(now.strftime("%Y%m%d%H%M%SZ"))
    cert.set_notAfter(valid_until.strftime("%Y%m%d%H%M%SZ"))

    cert.set_issuer(ca.get_subject())

    cert.set_pubkey(client_public_key)

    cert.sign(ca_key, 'sha1')

    return cert
