from django.shortcuts import render
from models import Contact, HttpLogEntry


def index(request):
    try:
        contacts = Contact.objects.get(pk=1)
    except Contact.DoesNotExist:
        contacts = None

    data = {
        'contacts': contacts,
    }
    return render(request, 'index.html', data)


def get_http_log(request):
    try:
        log = HttpLogEntry.objects.all().order_by('-pk')[:10]
    except HttpLogEntry.DoesNotExist:
        log = None
    data = {
        'log': log,
        'host': request.get_host(),
    }
    return render(request, 'requests.html', data)
