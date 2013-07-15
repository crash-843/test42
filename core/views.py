from django.shortcuts import render
from models import Contact


def index(request):
    try:
        contacts = Contact.objects.get(pk=1)
    except Contact.DoesNotExist:
        contacts = None

    data = {
        'contacts': contacts,
    }
    return render(request, 'index.html', data)
