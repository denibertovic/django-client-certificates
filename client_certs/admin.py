from django.contrib import admin

from .models import Cert


class CertAdmin(admin.ModelAdmin):

    list_display = ('user', 'install_link', 'is_valid', 'valid_until', 'is_installed')
    fields = ('user', 'country', 'state', 'locality', 'organization',
        'organizational_unit', 'common_name', 'description', 'valid_until')

    def install_link(self, obj):
        return '<a href="%s">Install Link</a>' % obj.get_absolute_url()
    install_link.allow_tags = True

admin.site.register(Cert, CertAdmin)
