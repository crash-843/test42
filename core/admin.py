from django.contrib import admin

from models import Contact, HttpLogEntry, ModelsChangeLog

admin.site.register(Contact)
admin.site.register(HttpLogEntry)
admin.site.register(ModelsChangeLog)
