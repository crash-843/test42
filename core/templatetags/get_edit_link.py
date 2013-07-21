from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template import Library

register = Library()


@register.simple_tag
def edit_link(obj):
    if obj:
        obj_type = ContentType.objects.get_for_model(obj)
        obj_link = reverse("admin:%s_%s_change" % (obj_type.app_label, obj_type.model), args=(obj.pk,))
        obj_full_link = '<a href="%s">edit (%s)</a>' % (obj_link, obj)
        return obj_full_link
    else:
        return ''
