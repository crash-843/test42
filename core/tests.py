from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from models import Contact


class ContactTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        contact = Contact.objects.get(pk=1)
        self.assertEqual(contact.first_name, 'Igor')
        self.assertEqual(contact.last_name, 'Kucher')
        self.assertEqual(contact.birth_date.strftime("%Y-%m-%d"), '1990-01-15')
        self.assertEqual(contact.bio, 'biography')
        self.assertEqual(contact.email, 'igor.k.843@gmail.com')
        self.assertEqual(contact.jabber, 'crash843@khavr.com')
        self.assertEqual(contact.info.skype, "iggor_ua")
        self.assertEqual(contact.info.other_contacts, "other_contacts")
