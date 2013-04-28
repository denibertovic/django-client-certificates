from django.core.mail import EmailMessage
from django.conf import settings
from OpenSSL import crypto

from .cert import export_client_cert_as_pk12


def send_p12_files_via_email(queryset):
    for cert in queryset:
        p12_file = export_client_cert_as_pk12(
            crypto.load_certificate(crypto.FILETYPE_PEM, cert.x509),
            cert.export_password)
        email = EmailMessage('Your PKCS12 Certificate', 'Please see attachment',
            settings.DEFAULT_FROM_EMAIL,
            [cert.user.email])
        email.attach(cert.user.username + '.p12', p12_file, 'application/x-pkcs12')
        email.send()
    return True
