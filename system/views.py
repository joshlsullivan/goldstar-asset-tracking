from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views import View
from client.models import System, Job
from datetime import datetime

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
        today = datetime.today()
        current_year = today.year
        previous_year = current_year - 1
        current_month = today.month
        contracted = Systems.objects.filter(contracted='Y')
        non-contracted = Systems.objects.filter(contracted='N')
        maintenance = Systems.objects.filter()
        total_jobs = Job.objects.all()
        total_maintenance_jobs = Job.objects.filter(job_category="Maintenance")
        systems = System.objects.all()
        return render(
            request,
            'system/kpi_report.html',
            {
                'systems':systems,
                'current_year':current_year,
                'previous_year':previous_year,
                'current_month':current_month,
                'total_jobs':total_jobs,
                'total_maintenance_jobs':total_maintenance_jobs,
                'today':today,
                'contracted':contracted,
                'non-contracted':non-contracted,
                'maintenance':maintenance,
            }
        )
