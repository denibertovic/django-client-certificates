from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .widgets import KeygenWidget


class InstallCertificateForm(AuthenticationForm):
    pub_key = forms.CharField(widget=KeygenWidget)
