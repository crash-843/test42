from django.db.models.signals import post_save, post_delete

from models import ModelsChangeLog


def save_callback(sender, **kwargs):
    if sender != ModelsChangeLog:
        if kwargs.get('created'):
            entry = ModelsChangeLog(model=sender.__name__, action=ModelsChangeLog.CREATE)
        else:
            entry = ModelsChangeLog(model=sender.__name__, action=ModelsChangeLog.EDIT)
        entry.save()


def delete_callback(sender, **kwargs):
    if sender != ModelsChangeLog:
        entry = ModelsChangeLog(model=sender.__name__, action=ModelsChangeLog.DELETE)
        entry.save()

post_save.connect(save_callback)
post_delete.connect(delete_callback)
