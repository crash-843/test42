from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from models import Contact, HttpLogEntry


class ContactTest(TestCase):
    fixtures = ['fixture.json']

    def test_contact(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Igor')
        self.assertContains(response, 'Kucher')
        self.assertContains(response, '15.01.1990')
        self.assertContains(response, 'biography<br />biography')
        self.assertContains(response, 'igor.k.843@gmail.com')
        self.assertContains(response, 'crash843@khavr.com')
        self.assertContains(response, 'iggor_ua')
        self.assertContains(response, "contacts<br />contacts")


class HttpMiddlewareTestCase(TestCase):
    """test middleware that stored all http requests in the DB"""
    def test_midelware(self):
        response = self.client.get(reverse('index'))
        log_entry = HttpLogEntry.objects.latest('pk')
        self.assertEqual(log_entry.url, reverse('index'))
