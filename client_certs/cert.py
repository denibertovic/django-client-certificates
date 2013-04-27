from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join

CERT_FILE = "/tmp/myapp.crt"
KEY_FILE = "/tmp/myapp.key"
P12_FILE = "/tmp/myapp.p12"


def create_self_signed_cert():
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "Minnesota"
    cert.get_subject().L = "Minnetonka"
    cert.get_subject().O = "my company"
    cert.get_subject().OU = "my organization"
    cert.get_subject().CN = gethostname()
    cert.get_subject().emailAddress = "deni@kset.org"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    open(CERT_FILE, "wt").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(KEY_FILE, "wt").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    p12 = crypto.PKCS12()
    p12.set_privatekey(k)
    p12.set_certificate(cert)
    open(P12_FILE, 'wb').write(p12.export(passphrase="dinamo"))

create_self_signed_cert()
