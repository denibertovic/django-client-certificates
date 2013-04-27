from django.shortcuts import render
import re
from django.contrib.auth.models import User


def index(request):
    client_certificate_info = request.META.get('HTTP_X_CLIENT_DN')
    found = re.search('emailAddress=(.+)', client_certificate_info)
    user = None
    if found:
        email = found.group(1)
        user = User.objects.get(email=email)
    return render(request, 'index.html', {'cert_user': user})
