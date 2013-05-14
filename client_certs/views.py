import string
import re

from django.http import HttpResponse
from django.shortcuts import render

from OpenSSL import crypto

from .cert import create_self_signed_client_cert
from .forms import InstallCertificateForm
from .models import Cert


def install_certificate(request, uuid):
    if request.method == "POST":
        form = InstallCertificateForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            try:
                cert = Cert.objects.get(user=user, uuid=uuid, is_installed=False)
            except Cert.DoesNotExist:
                raise

            regex = re.compile(r'[ \t\n\r\0\x0B]')
            pub_key = form.cleaned_data.get('pub_key')
            pub_key = regex.sub('', pub_key)

            spki = crypto.NetscapeSPKI(pub_key)
            cert.pub_key = pub_key
            x509 = create_self_signed_client_cert(
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

            ret = HttpResponse(mimetype="application/x-x509-user-cert")
            ret.write(crypto.dump_certificate(crypto.FILETYPE_ASN1, x509))
            return ret
    else:
        form = InstallCertificateForm(request=request)

    request.session.set_test_cookie()

    return render(request, 'client_certs/install_certificate.html', {'form': form})
