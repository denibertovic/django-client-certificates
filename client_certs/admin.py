from django.contrib import admin
from .models import Cert


class CertAdmin(admin.ModelAdmin):
    list_display = ('user',)
    fields = ('user', 'export_password', 'country', 'state', 'locality',
        'organization', 'organizational_unit', 'common_name')

admin.site.register(Cert, CertAdmin)
