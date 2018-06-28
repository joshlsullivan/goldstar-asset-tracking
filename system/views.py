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
        jan_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='01').filter(contracted='Y').count()
        feb_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='02').filter(contracted='Y').count()
        mar_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='03').filter(contracted='Y').count()
        apr_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='04').filter(contracted='Y').count()
        may_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='05').filter(contracted='Y').count()
        jun_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='06').filter(contracted='Y').count()
        jul_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='07').filter(contracted='Y').count()
        aug_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='08').filter(contracted='Y').count()
        sep_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='09').filter(contracted='Y').count()
        oct_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='10').filter(contracted='Y').count()
        nov_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='11').filter(contracted='Y').count()
        dec_cur_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='12').filter(contracted='Y').count()
        jan_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='01').filter(contracted='N').count()
        feb_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='02').filter(contracted='N').count()
        mar_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='03').filter(contracted='N').count()
        apr_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='04').filter(contracted='N').count()
        may_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='05').filter(contracted='N').count()
        jun_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='06').filter(contracted='N').count()
        jul_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='07').filter(contracted='N').count()
        aug_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='08').filter(contracted='N').count()
        sep_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='09').filter(contracted='N').count()
        oct_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='10').filter(contracted='N').count()
        nov_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='11').filter(contracted='N').count()
        dec_cur_non_con = System.objects.filter(contract_date__year=current_year).filter(contract_date__month='12').filter(contracted='N').count()
        jan_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='01').filter(job_category='Maintenance').count()
        feb_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='02').filter(job_category='Maintenance').count()
        mar_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='03').filter(job_category='Maintenance').count()
        apr_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='04').filter(job_category='Maintenance').count()
        may_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='05').filter(job_category='Maintenance').count()
        jun_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='06').filter(job_category='Maintenance').count()
        jul_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='07').filter(job_category='Maintenance').count()
        aug_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='08').filter(job_category='Maintenance').count()
        sep_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='09').filter(job_category='Maintenance').count()
        oct_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='10').filter(job_category='Maintenance').count()
        nov_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='11').filter(job_category='Maintenance').count()
        dec_cur_man = Job.objects.filter(job_date__year=current_year).filter(job_date__month='12').filter(job_category='Maintenance').count()
        # Previous year
        jan_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='01').filter(contracted='Y').count()
        feb_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='02').filter(contracted='Y').count()
        mar_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='03').filter(contracted='Y').count()
        apr_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='04').filter(contracted='Y').count()
        may_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='05').filter(contracted='Y').count()
        jun_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='06').filter(contracted='Y').count()
        jul_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='07').filter(contracted='Y').count()
        aug_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='08').filter(contracted='Y').count()
        sep_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='09').filter(contracted='Y').count()
        oct_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='10').filter(contracted='Y').count()
        nov_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='11').filter(contracted='Y').count()
        dec_pre_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='12').filter(contracted='Y').count()
        jan_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='01').filter(contracted='N').count()
        feb_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='02').filter(contracted='N').count()
        mar_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='03').filter(contracted='N').count()
        apr_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='04').filter(contracted='N').count()
        may_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='05').filter(contracted='N').count()
        jun_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='06').filter(contracted='N').count()
        jul_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='07').filter(contracted='N').count()
        aug_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='08').filter(contracted='N').count()
        sep_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='09').filter(contracted='N').count()
        oct_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='10').filter(contracted='N').count()
        nov_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='11').filter(contracted='N').count()
        dec_pre_non_con = System.objects.filter(contract_date__year=previous_year).filter(contract_date__month='12').filter(contracted='N').count()
        jan_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='01').filter(job_category='Maintenance').count()
        feb_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='02').filter(job_category='Maintenance').count()
        mar_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='03').filter(job_category='Maintenance').count()
        apr_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='04').filter(job_category='Maintenance').count()
        may_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='05').filter(job_category='Maintenance').count()
        jun_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='06').filter(job_category='Maintenance').count()
        jul_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='07').filter(job_category='Maintenance').count()
        aug_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='08').filter(job_category='Maintenance').count()
        sep_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='09').filter(job_category='Maintenance').count()
        oct_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='10').filter(job_category='Maintenance').count()
        nov_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='11').filter(job_category='Maintenance').count()
        dec_pre_man = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='12').filter(job_category='Maintenance').count()
        return render(
            request,
            'system/kpi_report.html',
            {
                'current_year':current_year,
                'previous_year':previous_year,
                'jan_cur_con':jan_cur_con,
                'feb_cur_con':feb_cur_con,
                'mar_cur_con':mar_cur_con,
                'apr_cur_con':apr_cur_con,
                'may_cur_con':may_cur_con,
                'jun_cur_con':jun_cur_con,
                'jul_cur_con':jul_cur_con,
                'aug_cur_con':aug_cur_con,
                'sep_cur_con':sep_cur_con,
                'oct_cur_con':oct_cur_con,
                'nov_cur_con':nov_cur_con,
                'dec_cur_con':dec_cur_con,
                'jan_cur_non_con':jan_cur_non_con,
                'feb_cur_non_con':feb_cur_non_con,
                'mar_cur_non_con':mar_cur_non_con,
                'apr_cur_non_con':apr_cur_non_con,
                'may_cur_non_con':may_cur_non_con,
                'jun_cur_non_con':jun_cur_non_con,
                'jul_cur_non_con':jul_cur_non_con,
                'aug_cur_non_con':aug_cur_non_con,
                'sep_cur_non_con':sep_cur_non_con,
                'oct_cur_non_con':oct_cur_non_con,
                'nov_cur_non_con':nov_cur_non_con,
                'dec_cur_non_con':dec_cur_non_con,
                'jan_cur_man':jan_cur_man,
                'feb_cur_man':feb_cur_man,
                'mar_cur_man':mar_cur_man,
                'apr_cur_man':apr_cur_man,
                'may_cur_man':may_cur_man,
                'jun_cur_man':jun_cur_man,
                'jul_cur_man':jul_cur_man,
                'aug_cur_man':aug_cur_man,
                'sep_cur_man':sep_cur_man,
                'oct_cur_man':oct_cur_man,
                'nov_cur_man':nov_cur_man,
                'dec_cur_man':dec_cur_man,
                'jan_pre_con':jan_pre_con,
                'feb_pre_con':feb_pre_con,
                'mar_pre_con':mar_pre_con,
                'apr_pre_con':apr_pre_con,
                'may_pre_con':may_pre_con,
                'jun_pre_con':jun_pre_con,
                'jul_pre_con':jul_pre_con,
                'aug_pre_con':aug_pre_con,
                'sep_pre_con':sep_pre_con,
                'oct_pre_con':oct_pre_con,
                'nov_pre_con':nov_pre_con,
                'dec_pre_con':dec_pre_con,
                'jan_pre_non_con':jan_pre_non_con,
                'feb_pre_non_con':feb_pre_non_con,
                'mar_pre_non_con':mar_pre_non_con,
                'apr_pre_non_con':apr_pre_non_con,
                'may_pre_non_con':may_pre_non_con,
                'jun_pre_non_con':jun_pre_non_con,
                'jul_pre_non_con':jul_pre_non_con,
                'aug_pre_non_con':aug_pre_non_con,
                'sep_pre_non_con':sep_pre_non_con,
                'oct_pre_non_con':oct_pre_non_con,
                'nov_pre_non_con':nov_pre_non_con,
                'dec_pre_non_con':dec_pre_non_con,
                'jan_pre_man':jan_pre_man,
                'feb_pre_man':feb_pre_man,
                'mar_pre_man':mar_pre_man,
                'apr_pre_man':apr_pre_man,
                'may_pre_man':may_pre_man,
                'jun_pre_man':jun_pre_man,
                'jul_pre_man':jul_pre_man,
                'aug_pre_man':aug_pre_man,
                'sep_pre_man':sep_pre_man,
                'oct_pre_man':oct_pre_man,
                'nov_pre_man':nov_pre_man,
                'dec_pre_man':dec_pre_man,
            }
        )
