from django.db import models
from django.utils.translation import ugettext as _


class Contact(models.Model):
    first_name = models.CharField(_("Name"), max_length=32)
    last_name = models.CharField(_("Last name"), max_length=32)
    birth_date = models.DateField(_("Date of birth"))
    bio = models.TextField(_("Bio"))
    email = models.EmailField(_("E-mail"), max_length=255, unique=True)
    jabber = models.CharField(_("Jabber"), max_length=255)
    skype = models.CharField(_("Skype"), max_length=32)
    other_contacts = models.TextField(_("Other contacts"))


class HttpLogEntry(models.Model):
    url = models.URLField(_("Url"))
