from django.contrib import admin
from .models import Cert
from django.contrib import messages
from .services import send_p12_files_via_email


class CertAdmin(admin.ModelAdmin):
    list_display = ('user',)
    fields = ('user', 'export_password', 'country', 'state', 'locality',
        'organization', 'organizational_unit', 'common_name')

    def send_p12(self, request, queryset):
        resp = send_p12_files_via_email(queryset)
        if resp:
            self.message_user(request, "PKCS12 certificates have been sent.")
        else:
            self.message_user(request,
                "An error happend.",
                level=messages.INFO)

    send_p12.short_description = "Export Certificate and send via email"

    actions = [send_p12]

admin.site.register(Cert, CertAdmin)
