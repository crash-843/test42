from django.conf import settings


def settings_to_context(request):
    return {'settings': settings}
