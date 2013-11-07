import logging
from datetime import datetime
import uuid

from django.conf import settings

from OpenSSL import crypto

from .helpers import asn1_general_time_format


log = logging.getLogger(__name__)


def create_signed_client_cert(client_public_key, country, state, locality, organization,
        organizational_unit, common_name, email, valid_until):
    """
    Function for generating client certificates
    """

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

    cert.set_notBefore(asn1_general_time_format(now))
    cert.set_notAfter(asn1_general_time_format(valid_until))

    cert.set_issuer(ca.get_subject())

    cert.set_pubkey(client_public_key)

    cert.sign(ca_key, 'sha1')

    return cert


def revoke_certificates(certificates):
    try:
        with open(settings.CERT_CA_FILE) as ca_file:
            ca = crypto.load_certificate(crypto.FILETYPE_PEM, ca_file.read())
        with open(settings.CERT_CA_KEY_FILE) as ca_key_file:
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key_file.read())
    except IOError as e:
        log.error(e)
        raise

    with open(settings.CERT_REVOKE_FILE, 'r') as f:
        crl = crypto.load_crl(crypto.FILETYPE_PEM, f.read())
        for cert in certificates:
            x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            revoked = crypto.Revoked()
            revoked.set_rev_date(asn1_general_time_format(datetime.now()))
            revoked.set_serial(hex(x509.get_serial_number())[2:])
            crl.add_revoked(revoked)
        crl_text = crl.export(ca, ca_key)
    with open(settings.CERT_REVOKE_FILE, 'w') as f:
        f.write(crl_text)
