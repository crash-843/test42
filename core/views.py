from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import ContactForm
from models import Contact, HttpLogEntry


def index(request):
    try:
        contacts = Contact.objects.get(pk=1)
    except Contact.DoesNotExist:
        contacts = None

    data = {
        'contacts': contacts,
    }
    return render(request, 'core/index.html', data)


def get_http_log(request):
    try:
        log = HttpLogEntry.objects.all().order_by('created')[:10]
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
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ContactForm(instance=contact)
        data = {
            'form': form,
        }
        return render(request, 'core/contact_edit.html', data)
    data = {
        'form': form,
    }
    return render(request, 'core/contact_edit.html', data)
