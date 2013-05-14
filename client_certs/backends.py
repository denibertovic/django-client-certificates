from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
import hashlib


def get_md5_hexdigest(email):
    """
    Returns an md5 hash for a given email.

    The length is 30 so that it fits into Django's ``User.username`` field.

    """
    return hashlib.md5(email).hexdigest()[0:30]


class ClientCertificateBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``ClientCertificateMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    emails that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """

    # Create a User object if not already in the database?
    create_unknown_user = True

    def authenticate(self, email):
        """
        The email address passed as ``email`` is considered trusted.  This
        method simply returns the ``User`` object with the given email,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given email is not found in the database.
        """
        if not email:
            return
        user = None
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            if self.create_unknown_user:
                user = UserModel.objects.create(
                            username=get_md5_hexdigest(email),
                            email=email)
        return user
