import os
from StringIO import StringIO

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.template.defaultfilters import linebreaksbr
from django.test import TestCase

from models import Contact, HttpLogEntry, ModelsChangeLog


class ContactTest(TestCase):
    def test_contact(self):
        response = self.client.get(reverse('index'))
        contact = Contact.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, contact.first_name)
        self.assertContains(response, contact.last_name)
        self.assertContains(response, contact.birth_date.strftime("%d.%m.%Y"))
        self.assertContains(response, linebreaksbr(contact.bio))
        self.assertContains(response, contact.email)
        self.assertContains(response, contact.jabber)
        self.assertContains(response, contact.skype)
        self.assertContains(response, linebreaksbr(contact.other_contacts))


class HttpMiddlewareTestCase(TestCase):
    """test middleware that stored all http requests in the DB"""
    def test_new_entry(self):
        response = self.client.get(reverse('index'))
        log_entry = HttpLogEntry.objects.latest('created')
        self.assertEqual(log_entry.url, reverse('index'))
        self.assertEqual(log_entry.method, 'GET')
        self.assertEqual(log_entry.status_code, response.status_code)

    def test_view(self):
        for i in range(1, 15):
            response = self.client.get(reverse('index'))
            response = self.client.get(reverse('log'))

        response = self.client.get(reverse('log'))
        log = HttpLogEntry.objects.all().order_by('created')[:10]
        log_resp = response.context['log']

        self.assertEqual(len(log_resp), 10)
        for i in range(0, 10):
            self.assertEqual(log[i].url, log_resp[i].url)
            self.assertEqual(log[i].method, log_resp[i].method)
            self.assertEqual(log[i].status_code, log_resp[i].status_code)
            self.assertEqual(log[i].created, log_resp[i].created)


class ContextProcessorsTextCase(TestCase):
    def test_context_processor(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['settings'], settings)


class ContactEditTestCase(TestCase):
    def test_edit_form(self):
        response = self.client.get(reverse('contact-edit'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('contact-edit'))
        self.assertEqual(response.status_code, 200)

        data = Contact.objects.values().get(pk=1)
        data['first_name'] = 'Igor_test'
        data['last_name'] = 'Kucher_test'
        data['birth_date'] = '1990-01-10'
        data['email'] = 'test@domain.com'
        data['jabber'] = 'testt@domain.com'
        data['skype'] = 'skype_test'
        data['other_contacts'] = 'other_test'
        data['bio'] = 'bio_test'
        data['photo'] = open(os.path.join(settings.MEDIA_ROOT, 'images/core/test_image.jpg'), "rb")

        response = self.client.post(reverse('contact-edit'), data)
        self.assertEqual(response.status_code, 302)

        contact = Contact.objects.get(pk=1)
        self.assertEqual(contact.first_name, data['first_name'])
        self.assertEqual(contact.last_name, data['last_name'])
        self.assertEqual(contact.birth_date.strftime("%Y-%m-%d"), data['birth_date'])
        self.assertEqual(contact.email, data['email'])
        self.assertEqual(contact.jabber, data['jabber'])
        self.assertEqual(contact.skype, data['skype'])
        self.assertEqual(contact.other_contacts, data['other_contacts'])
        self.assertEqual(contact.bio, data['bio'])

    def test_ajax_edit_form(self):
        self.client.login(username='admin', password='admin')

        data = Contact.objects.values().get(pk=1)
        data['first_name'] = 'Igor_test'
        data['last_name'] = 'Kucher_test'
        data['birth_date'] = '1990-01-10'
        data['email'] = 'test@domain.com'
        data['jabber'] = 'testt@domain.com'
        data['skype'] = 'skype_test'
        data['other_contacts'] = 'other_test'
        data['bio'] = 'bio_test'
        data['photo'] = open(os.path.join(settings.MEDIA_ROOT, 'images/core/test_image.jpg'), "rb")

        response = self.client.post(reverse('contact-edit'), data,  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"is_error": 0')

        contact = Contact.objects.get(pk=1)
        self.assertEqual(contact.first_name, data['first_name'])
        self.assertEqual(contact.last_name, data['last_name'])
        self.assertEqual(contact.birth_date.strftime("%Y-%m-%d"), data['birth_date'])
        self.assertEqual(contact.email, data['email'])
        self.assertEqual(contact.jabber, data['jabber'])
        self.assertEqual(contact.skype, data['skype'])
        self.assertEqual(contact.other_contacts, data['other_contacts'])
        self.assertEqual(contact.bio, data['bio'])


class EditLinkTemplateTagTestCase(TestCase):
    def test_edit_tag(self):
        contact = Contact.objects.get(pk=1)
        link = reverse("admin:core_contact_change", args=(contact.pk,))
        full_link = '<a href="%s">edit (%s)</a>' % (link, contact)
        template = "{% load get_edit_link %} {% edit_link contact %}"
        data = {
            'contact': contact,
        }
        response = Template(template).render(Context(data))
        self.assertEqual(response.strip(), full_link)


class GetModelsComandTestCase(TestCase):
    def test_det_models(self):
        stdout = StringIO()
        stderr = StringIO()

        call_command('get_models', stdout=stdout, stderr=stderr)

        stdout.seek(0)
        stderr.seek(0)
        stdout = stdout.read()
        stderr = stderr.read()

        models_list = ''
        models_list_err = ''

        for model in ContentType.objects.all():
            out = '%s - %s' % (model.model, model.model_class().objects.count())
            models_list = models_list + out + '\n'
            models_list_err = models_list_err + out + '\n'

        self.assertEqual(stdout, models_list)
        self.assertEqual(stdout, models_list_err)


class ModelsChangeLogTestCase(TestCase):
    def test_signal_processor(self):
        contact = Contact(
            first_name='Igor_test',
            last_name='Kucher_test',
            birth_date='1990-01-10',
            email='test@domain.com',
            jabber='testt@domain.com',
            skype='skype_test',
            other_contacts='other_test',
            bio='bio_test'
        )
        contact.save()

        log_entry = ModelsChangeLog.objects.latest()
        self.assertEqual(log_entry.model, contact._meta.object_name)
        self.assertEqual(log_entry.action, ModelsChangeLog.CREATE)

        contact.first_name = 'Igor_test_edit'
        contact.save()
        log_entry = ModelsChangeLog.objects.latest()
        self.assertEqual(log_entry.model, contact._meta.object_name)
        self.assertEqual(log_entry.action, ModelsChangeLog.EDIT)

        contact.delete()
        log_entry = ModelsChangeLog.objects.latest('created')
        self.assertEqual(log_entry.model, contact._meta.object_name)
        self.assertEqual(log_entry.action, ModelsChangeLog.DELETE)
