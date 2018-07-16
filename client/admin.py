from django.contrib import admin
from .models import Client, Job, Task, System

class ClientAdmin(admin.ModelsAdmin):
    list_display = ('name')
    search_fields = ['name']

class SystemAdmin(admin.ModelsAdmin):
    list_display = ['client', 'get_system_type_display']

admin.site.register(Client, ClientAdmin)
admin.site.register(System, SystemAdmin)
