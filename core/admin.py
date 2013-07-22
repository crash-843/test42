from django.contrib import admin

from models import Contact, HttpLogEntry, ModelsChangeLog


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'birth_date',)


class HttpLogEntryAdmin(admin.ModelAdmin):
    list_display = ('url', 'method', 'status_code', 'priority', 'created',)
    list_editable = ('priority',)
    list_filter = ('method', 'status_code', )


class ModelsChangeLogAdmin(admin.ModelAdmin):
    list_display = ('model', 'action', 'created',)
    list_filter = ('action', 'model', )

admin.site.register(Contact, ContactAdmin)
admin.site.register(HttpLogEntry, HttpLogEntryAdmin)
admin.site.register(ModelsChangeLog, ModelsChangeLogAdmin)
