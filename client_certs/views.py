from django.http import HttpResponse
from django.shortcuts import render

from OpenSSL import crypto

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
                return HttpResponse(
                    content='Certificate could not be found for this user or was already installed!',
                    status=400)

            x509 = cert.generate_and_sign_client_cert(
                pub_key=form.cleaned_data.get('pub_key'))

            ret = HttpResponse(mimetype="application/x-x509-user-cert")
            ret.write(crypto.dump_certificate(crypto.FILETYPE_ASN1, x509))
            return ret
    else:
        form = InstallCertificateForm(request=request)

    return render(request, 'client_certs/install_certificate.html', {'form': form})
