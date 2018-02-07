from django.contrib import admin
from .models import Client, Job, Task, System

@admin.register(Client, Job, Task, System)
class ClientAdmin(admin.ModelAdmin):
    pass
