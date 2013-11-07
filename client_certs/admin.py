from django.contrib import admin

from .models import Cert
from .cert import revoke_certificates


class CertAdmin(admin.ModelAdmin):

    list_display = ('user', 'install_link', 'is_valid', 'valid_until')
    fields = ('user', 'country', 'state', 'locality', 'organization',
        'organizational_unit', 'common_name', 'description', 'valid_until')

    def install_link(self, obj):
        return '<a href="%s">Install Link</a>' % obj.get_absolute_url()
    install_link.allow_tags = True

    def revoke_certificate(self, request, queryset):
        for_revokation = [cert.x509 for cert in queryset if cert.is_valid and cert.is_installed]
        revoke_certificates(for_revokation)

        updated = queryset.update(is_valid=False)
        if updated == 1:
            message = '1 Certificate was revoked.'
        else:
            message = '%s Certificates were revoked.' % updated

        self.message_user(request, message)

    revoke_certificate.short_description = "Revoke selected Client Certificates"

    actions = [revoke_certificate]

admin.site.register(Cert, CertAdmin)
