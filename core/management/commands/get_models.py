from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Show project models list and the count of objects in every model'

    def handle(self, *args, **options):
        for model in ContentType.objects.all():
            out = '%s - %s' % (model.model, model.model_class().objects.count())
            self.stdout.write(out)
            self.stderr.write('error: %s' % out)
