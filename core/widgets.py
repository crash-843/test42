from django.forms import DateInput
from django.conf import settings
from django.utils.safestring import mark_safe


class DateWidget(DateInput):
    def __init__(self, params='', attrs=None):
        self.params = params
        super(DateWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(DateWidget, self).render(name, value, attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').datepicker({%s});
            </script>''' % (name, self.params,))

    class Media:
        css = {
            'all': (settings.STATIC_URL+"/css/jquery-ui/jquery-ui.min.css",)
        }
        js = (
            settings.STATIC_URL+"js/jquery-ui.min.js",
        )
