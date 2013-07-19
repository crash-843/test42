from django.contrib import admin

from models import Contact, HttpLogEntry

admin.site.register(Contact)
admin.site.register(HttpLogEntry)
