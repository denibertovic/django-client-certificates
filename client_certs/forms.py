import re

from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .widgets import KeygenWidget


class InstallCertificateForm(AuthenticationForm):
    pub_key = forms.CharField(widget=KeygenWidget)

    def clean_pub_key(self):
        regex = re.compile(r'[ \t\n\r\0\x0B]')
        pub_key = regex.sub('', self.cleaned_data['pub_key'])

        return pub_key
