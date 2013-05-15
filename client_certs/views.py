from django.http import HttpResponse
from django.shortcuts import render

from OpenSSL import crypto

from .forms import InstallCertificateForm
from .helpers import create_x509_and_update_cert


def install_certificate(request, uuid):
    if request.method == "POST":
        form = InstallCertificateForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            x509 = create_x509_and_update_cert(
                        user=user,
                        uuid=uuid,
                        pub_key=form.cleaned_data.get('pub_key'))
            if not x509:
                return HttpResponse(content='Invalid or already installed Client Certificate', status=404)
            ret = HttpResponse(mimetype="application/x-x509-user-cert")
            ret.write(crypto.dump_certificate(crypto.FILETYPE_ASN1, x509))
            return ret
    else:
        form = InstallCertificateForm(request=request)

    request.session.set_test_cookie()

    return render(request, 'client_certs/install_certificate.html', {'form': form})
