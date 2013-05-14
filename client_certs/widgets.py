from django.forms.widgets import Input
from django.utils.html import format_html
from django.forms.util import flatatt


class KeygenWidget(Input):
    input_type = 'hidden'
    is_hidden = True

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        return format_html('<keygen{0} hidden=true>', flatatt(final_attrs))
