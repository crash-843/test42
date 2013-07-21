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
    photo = models.ImageField(_('Photo'), upload_to="images/core/upload", null=True, blank=True)

    def __unicode__(self):
        return self.first_name


class HttpLogEntry(models.Model):
    url = models.URLField(_("Url"))
    method = models.CharField(_("Method"), max_length=10)
    status_code = models.IntegerField(_("Status code"))
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.url


class ModelsChangeLog(models.Model):
    CREATE = 0
    EDIT = 1
    DELETE = 2

    ACTION_CHOICES = (
        (CREATE, _("Created")),
        (EDIT, _("Edited")),
        (DELETE, _("Deleted")),
    )

    model = models.CharField(max_length=255)
    action = models.IntegerField(choices=ACTION_CHOICES)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return "%s - %s at %s" % (self.model, self.get_action_display(), self.created.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        get_latest_by = "created"
