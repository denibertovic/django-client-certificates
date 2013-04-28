from django.contrib import auth
from django.contrib.auth import load_backend
from django.core.exceptions import ImproperlyConfigured

from .backends import ClientCertificateBackend

import re


class ClientCertificateMiddleware(object):
    """
    Check for client certificate and log user in automatically

    """

    header = 'HTTP_X_CLIENT_DN'

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django client certificate user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the ClientCertificateMiddleware class.")
        try:
            client_certificate_info = request.META[self.header]
            if client_certificate_info:
                found = re.search('emailAddress=(.+)', client_certificate_info)
                if found:
                    email = found.group(1)
                else:
                    return
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                try:
                    stored_backend = load_backend(request.session.get(
                        auth.BACKEND_SESSION_KEY, ''))
                    if isinstance(stored_backend, ClientCertificateBackend):
                        auth.logout(request)
                except ImproperlyConfigured:
                    # backend failed to load
                    auth.logout(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.email == email:
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(email=email)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)
