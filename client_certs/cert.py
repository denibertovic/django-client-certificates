from OpenSSL import crypto
from django.conf import settings
from datetime import datetime, timedelta


import logging

log = logging.getLogger(__name__)


def create_self_signed_client_cert(country, state, locality, organization,
    organizational_unit, common_name, email):
    """
    Function for generating client certificates
    """

    # load files
    try:
        with open(settings.CERT_KEY_FILE) as key_file:
            k = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())
        with open(settings.CERT_CA_FILE) as ca_file:
            ca = crypto.load_certificate(crypto.FILETYPE_PEM, ca_file.read())
        with open(settings.CERT_CA_KEY_FILE) as ca_key_file:
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key_file.read())
    except IOError as e:
        log.error("Unable to open file: %s", e)
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

    cert.set_serial_number(1000)

    now = datetime.now()
    sooner = now - timedelta(days=1)
    later = now + timedelta(days=3650)

    cert.set_notBefore(sooner.strftime("%Y%m%d%H%M%SZ"))
    cert.set_notAfter(later.strftime("%Y%m%d%H%M%SZ"))

    cert.set_issuer(ca.get_subject())

    cert.set_pubkey(k)

    cert.sign(ca_key, 'sha1')

    ## to str for storing in db
    return crypto.dump_certificate(crypto.FILETYPE_PEM, cert)


def export_client_cert_as_pk12(cert, password):
    """
    Convert X509 cert to PKCS12
    """

    # load_key_file
    try:
        with open(settings.CERT_KEY_FILE) as key_file:
            k = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())
        with open(settings.CERT_CA_FILE) as ca_file:
            ca = crypto.load_certificate(crypto.FILETYPE_PEM, ca_file.read())
    except IOError as e:
        log.error("Unable to open file: %s", e)
        raise

    p12 = crypto.PKCS12()
    p12.set_privatekey(k)
    p12.set_certificate(cert)
    p12.set_ca_certificates([ca])
    return p12.export(passphrase=password)
