from django.template import Library
from django.core.urlresolvers import reverse

register = Library()


@register.simple_tag
def edit_link(obj):
    return reverse("admin:%s_%s_change" % (obj._meta.app_label, obj._meta.module_name), args=(obj.pk,))
