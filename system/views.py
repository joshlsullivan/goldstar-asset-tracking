from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from client.models import System

class SystemListView(LoginRequiredMixin, ListView):
    model = System
    fields = '__all__'
