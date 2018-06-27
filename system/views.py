from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views import View
from client.models import System

class SystemListView(LoginRequiredMixin, ListView):
    model = System
    fields = '__all__'
    template_name = 'system/system_list.html'

class MonitoringTypeListView(LoginRequiredMixin, ListView):
    template_name = 'system/monitoring_type_list.html'

    def get_queryset(self):
        self.monitoring_type = System.objects.filter(monitoring_type=self.kwargs['monitoring_type'])
        return self.monitoring_type

class SystemTypeListView(LoginRequiredMixin, ListView):
    template_name = 'system/system_type_list.html'

    def get_queryset(self):
        self.system_type = System.objects.filter(system_type=self.kwargs['system_type']).order_by('monitoring_type')
        print(self.system_type)
        return self.system_type

class SystemUpdateView(LoginRequiredMixin, UpdateView):
    model = System
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = '/systems/'

class SystemsKPIReport(View):
    def get(self, request, *args, **kwargs):
        systems = System.objects.all()
        return render(request, 'system/kip_report.html', {'systems':systems})
