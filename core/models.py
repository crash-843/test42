from django.db import models, DatabaseError
from django.db.models.signals import post_save, post_delete
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
    photo = models.ImageField(
        _('Photo'),
        upload_to="images/core/upload",
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.first_name


class HttpLogEntry(models.Model):
    url = models.URLField(_("Url"))
    method = models.CharField(_("Method"), max_length=10)
    status_code = models.IntegerField(_("Status code"))
    created = models.DateTimeField(
        _("Created"),
        auto_now_add=True,
        editable=False
    )
    priority = models.IntegerField(_("Priority"), default=0)

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ['-priority', 'created']


class ModelsChangeLog(models.Model):
    CREATE = 0
    EDIT = 1
    DELETE = 2

    ACTION_CHOICES = (
        (CREATE, _("Created")),
        (EDIT, _("Edited")),
        (DELETE, _("Deleted")),
    )

    model = models.CharField(_("Model"), max_length=255)
    action = models.IntegerField(_("Action"), choices=ACTION_CHOICES)
    created = models.DateTimeField(
        _("Created"),
        auto_now_add=True,
        editable=False
    )
    object_id = models.IntegerField(_("Object"), default=0)

    def __unicode__(self):
        return "%s - %s at %s" % (
            self.model,
            self.get_action_display(),
            self.created.strftime("%Y-%m-%d %H:%M:%S")
        )

    class Meta:
        get_latest_by = "created"


def save_callback(sender, created, instance, **kwargs):
    try:
        if sender != ModelsChangeLog:
            if isinstance(instance.pk, int):
                object_id = instance.pk
            else:
                object_id = 0

            if created:
                entry = ModelsChangeLog(
                    model=sender.__name__,
                    action=ModelsChangeLog.CREATE,
                    object_id=object_id
                )
            else:
                entry = ModelsChangeLog(
                    model=sender.__name__,
                    action=ModelsChangeLog.EDIT,
                    object_id=object_id
                )
            entry.save()
    except DatabaseError:
        pass


def delete_callback(sender, instance, **kwargs):
    try:
        if sender != ModelsChangeLog:
            if isinstance(instance.pk, int):
                object_id = instance.pk
            else:
                object_id = 0

            entry = ModelsChangeLog(
                model=sender.__name__,
                action=ModelsChangeLog.DELETE,
                object_id=object_id
            )
            entry.save()
    except DatabaseError:
        pass

post_save.connect(save_callback)
post_delete.connect(delete_callback)
