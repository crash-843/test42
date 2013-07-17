from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import linebreaksbr
from django.conf import settings
from models import Contact, HttpLogEntry


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
