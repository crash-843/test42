import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from forms import ContactForm
from models import Contact, HttpLogEntry


def index(request):
    try:
        contact = Contact.objects.get(pk=1)
    except Contact.DoesNotExist:
        contact = None

    data = {
        'contact': contact,
    }
    return render(request, 'core/index.html', data)


def get_http_log(request):
    try:
        log = HttpLogEntry.objects.all()[:10]
    except HttpLogEntry.DoesNotExist:
        log = None
    data = {
        'log': log,
        'host': request.get_host(),
    }
    return render(request, 'core/requests.html', data)


@login_required
def contact_edit(request):
    contact = Contact.objects.get(pk=1)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            if request.is_ajax():
                contact = form.save()
                try:
                    photo = contact.photo.url
                except ValueError:
                    photo = None
                data = {
                    'is_error': 0,
                    'photo': photo,
                }
                return HttpResponse(json.dumps(data))
            else:
                form.save()
                return HttpResponseRedirect(reverse('index'))
        else:
            if request.is_ajax():
                data = {
                    'is_error': 1,
                    'errors': form.errors,
                }
                return HttpResponse(json.dumps(data))
            else:
                data = {
                    'form': form,
                }
                return render(request, 'core/contact_edit.html', data)
    else:
        form = ContactForm(instance=contact)
        data = {
            'form': form,
        }
        return render(request, 'core/contact_edit.html', data)
