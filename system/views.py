from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from client.models import System

class SystemListView(LoginRequiredMixin, ListView):
    model = System
    fields = '__all__'
    template_name = 'system/system_list.html'

class MonitoringTypeListView(LoginRequiredMixin, ListView):
    template_name = 'system/monitoring_type_list.html'

    def get_queryset(self):
        self.system = get_object_or_404(System, monitoring_type=self.kwargs['monitoring_type'])
        return System.objects.filter(monitoring_type=self.system)
