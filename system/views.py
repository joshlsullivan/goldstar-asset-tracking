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
        jan_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='01').count()
        feb_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='02').count()
        mar_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='03').count()
        apr_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='04').count()
        may_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='05').count()
        jun_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='06').count()
        jul_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='07').count()
        aug_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='08').count()
        sep_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='09').count()
        oct_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='10').count()
        nov_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='11').count()
        dec_cur_jobs = Job.objects.filter(job_date__year=current_year).filter(job_date__month='12').count()
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
        jan_cur_rate = (jan_cur_man / jan_cur_jobs * 100) if jan_cur_jobs != 0 else 0
        feb_cur_rate = (feb_cur_man / feb_cur_jobs * 100) if feb_cur_jobs != 0 else 0
        mar_cur_rate = (mar_cur_man / mar_cur_jobs * 100) if mar_cur_jobs != 0 else 0
        apr_cur_rate = (apr_cur_man / apr_cur_jobs * 100) if apr_cur_jobs != 0 else 0
        may_cur_rate = (may_cur_man / may_cur_jobs * 100) if may_cur_jobs != 0 else 0
        jun_cur_rate = (jun_cur_man / jun_cur_jobs * 100) if jun_cur_jobs != 0 else 0
        jul_cur_rate = (jul_cur_man / jul_cur_jobs * 100) if jul_cur_jobs != 0 else 0
        aug_cur_rate = (aug_cur_man / aug_cur_jobs * 100) if aug_cur_jobs != 0 else 0
        sep_cur_rate = (sep_cur_man / sep_cur_jobs * 100) if sep_cur_jobs != 0 else 0
        oct_cur_rate = (oct_cur_man / oct_cur_jobs * 100) if oct_cur_jobs != 0 else 0
        nov_cur_rate = (nov_cur_man / nov_cur_jobs * 100) if nov_cur_jobs != 0 else 0
        dec_cur_rate = (dec_cur_man / dec_cur_jobs * 100) if dec_cur_jobs != 0 else 0
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
        jan_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='01').count()
        feb_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='02').count()
        mar_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='03').count()
        apr_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='04').count()
        may_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='05').count()
        jun_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='06').count()
        jul_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='07').count()
        aug_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='08').count()
        sep_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='09').count()
        oct_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='10').count()
        nov_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='11').count()
        dec_pre_jobs = Job.objects.filter(job_date__year=previous_year).filter(job_date__month='12').count()
        jan_pre_rate = (jan_pre_man / jan_pre_jobs * 100) if jan_pre_jobs != 0 else 0
        feb_pre_rate = (feb_pre_man / feb_pre_jobs * 100) if feb_pre_jobs != 0 else 0
        mar_pre_rate = (mar_pre_man / mar_pre_jobs * 100) if mar_pre_jobs != 0 else 0
        apr_pre_rate = (apr_pre_man / apr_pre_jobs * 100) if apr_pre_jobs != 0 else 0
        may_pre_rate = (may_pre_man / may_pre_jobs * 100) if may_pre_jobs != 0 else 0
        jun_pre_rate = (jun_pre_man / jun_pre_jobs * 100) if jun_pre_jobs != 0 else 0
        jul_pre_rate = (jul_pre_man / jul_pre_jobs * 100) if jul_pre_jobs != 0 else 0
        aug_pre_rate = (aug_pre_man / aug_pre_jobs * 100) if aug_pre_jobs != 0 else 0
        sep_pre_rate = (sep_pre_man / sep_pre_jobs * 100) if sep_pre_jobs != 0 else 0
        oct_pre_rate = (oct_pre_man / oct_pre_jobs * 100) if oct_pre_jobs != 0 else 0
        nov_pre_rate = (nov_pre_man / nov_pre_jobs * 100) if nov_pre_jobs != 0 else 0
        dec_pre_rate = (dec_pre_man / dec_pre_jobs * 100) if dec_pre_jobs != 0 else 0
        return render(
            request,
            'system/kpi_report.html',
            {
                'current_year':current_year,
                'previous_year':previous_year,
                'jan_cur_rate':jan_cur_rate,
                'feb_cur_rate':feb_cur_rate,
                'mar_cur_rate':mar_cur_rate,
                'apr_cur_rate':apr_cur_rate,
                'may_cur_rate':may_cur_rate,
                'jun_cur_rate':jun_cur_rate,
                'jul_cur_rate':jul_cur_rate,
                'aug_cur_rate':aug_cur_rate,
                'sep_cur_rate':sep_cur_rate,
                'oct_cur_rate':oct_cur_rate,
                'nov_cur_rate':nov_cur_rate,
                'dec_cur_rate':dec_cur_rate,
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
                'jan_pre_rate':jan_pre_rate,
                'feb_pre_rate':feb_pre_rate,
                'mar_pre_rate':mar_pre_rate,
                'apr_pre_rate':apr_pre_rate,
                'may_pre_rate':may_pre_rate,
                'jun_pre_rate':jun_pre_rate,
                'jul_pre_rate':jul_pre_rate,
                'aug_pre_rate':aug_pre_rate,
                'sep_pre_rate':sep_pre_rate,
                'oct_pre_rate':oct_pre_rate,
                'nov_pre_rate':nov_pre_rate,
                'dec_pre_rate':dec_pre_rate,
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
