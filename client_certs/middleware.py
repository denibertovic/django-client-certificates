from django.contrib.auth.models import User
from django.contrib.auth import login
import re


class ClientCertificateMiddleware(object):
    """
    Check for client certificate and log user in automatically

    """

    def process_request(self, request):
        client_certificate_info = request.META.get('HTTP_X_CLIENT_DN')
        found = re.search('emailAddress=(.+)', client_certificate_info)
        user = None
        if found:
            email = found.group(1)
            try:
                user = User.objects.get(email=email)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            except Exception as e:
                print e

        return None
