from django.contrib import admin
from core.models import Contact, HttpLogEntry


admin.site.register(Contact)
admin.site.register(HttpLogEntry)
