from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from urllib.parse import parse_qs
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models import Avg, Max, Min
import json
import jwt
import requests

import datetime
import pytz

from client.models import Client, Job, Task, System

auth = (settings.SERVICEM8_ADMIN_USERNAME, settings.SERVICEM8_ADMIN_PASSWORD)

def process_category(category_uuid):
    url = "https://api.servicem8.com/api_1.0/category/{}.json".format(category_uuid)
    #headers = {'Authorization':'Bearer {}'.format(token)}
    try:
        category = requests.get(url, auth=auth).json()
        name = category['name']
        print(name)
        return name
    except ValueError as e:
        print("Error - {}".format(e))
        pass

def process_task(customer_resource_url):
    url = customer_resource_url
    #headers = {'Authorization':'Bearer {}'.format(token)}
    r = requests.get(url, auth=auth)
    task = r.json()
    if task['task_complete'] == "0":
        print("Task is not complete")
    elif task['task_complete'] == "1":
        job = Job.objects.get(job_uuid=task['related_object_uuid'])
        job_created_time = job.created
        task_completed_time = datetime.datetime.strptime(task['completed_timestamp'], '%Y-%m-%d %H:%M:%S')
        task_due_date = datetime.datetime.strptime(task['due_date'], '%Y-%m-%d')
        task_completed_date = datetime.datetime.strptime(task['completed_timestamp'], '%Y-%m-%d %H:%M:%S')
        timezone = pytz.timezone('GB')
        date_aware_task_completed_time = timezone.localize(task_completed_time)
        date_aware_due_date = timezone.localize(task_due_date)
        date_aware_completed_date = timezone.localize(task_completed_date)
        job_task_time_difference = job_created_time - date_aware_task_completed_time
        days = job_task_time_difference.days
        days_to_hours = days * 24
        diff_btw_two_times = (job_task_time_difference.seconds) / 3600
        overall_hours = days_to_hours + diff_btw_two_times
        rounded_overall_hours = round(overall_hours, 2)
        t = job.task_set.create(task_uuid=task['uuid'], related_object_uuid=task['related_object_uuid'], due_date=date_aware_due_date, completed_date=date_aware_completed_date, job_task_time_difference=rounded_overall_hours)
        t.save()
        print("Time Job Create: {} | Time Task Completed: {} | Difference: {} hours".format(job_created_time, date_aware_task_completed_time, rounded_overall_hours))
        print("Job saved")
        return job

def process_client(customer_resource_url):
    #headers = {'Authorization': 'Bearer {}'.format(token)}
    print(customer_resource_url)
    client = requests.get(customer_resource_url, auth=auth).json()
    print("Client - {}".format(client))
    return client

def process_job(customer_resource_url):
    url = customer_resource_url
    #token=token
    #headers = {'Authorization':'Bearer {}'.format(token)}
    r = requests.get(url, auth=auth).json()
    print(r)
    name = r['name']
    client, created = Client.objects.get_or_create(
        client_uuid=r['company_uuid'],
        defaults={
            'name':name,
            'resource_url':url,
        }
    )
    print(client)
    job = Job(client=client, job_uuid=r['uuid'], job_category=process_category(r['category_uuid']))
    #j = client.job_set.create(job_uuid=job['uuid'])
    print("Job saved - {}".format(job))
    return job

# one-off function to populate jobs and clients
def load_client(company_uuid):
    url = 'https://api.servicem8.com/api_1.0/company/{}.json'.format(company_uuid)
    auth = ('josh+goldsmith@misllc.com', '9793')
    client = requests.get(url, auth=auth).json()
    return client

def load_jobs():
    url = 'https://api.servicem8.com/api_1.0/job.json'
    auth = ('josh+goldsmith@misllc.com', '9793')
    jobs = requests.get(url, auth=auth).json()
    for job in jobs:
        print(job)
        client = load_client(job['company_uuid'])
        print(client)
        try:
            obj1, created = Client.objects.get_or_create(
                client_uuid=client['uuid'],
                defaults={
                    'name':client['name'],
                    'resource_url':'https://api.servicem8.com/api_1.0/company/{}.json'.format(client['uuid']),
                }
            )
            print(obj1)
            obj2, created = Job.objects.get_or_create(
                job_uuid=obj1,
                defaults={
                    'client':job['company_uuid'],
                    'job_category':process_category(job['category_uuid']),
                    'job_date':job['date'],
                }
            )
            print(obj2)
            print("Saving job")
        except ValueError:
            pass
    return job

@csrf_exempt
def asset_tracking_event(request):
    encoded_token = request.body.decode("utf-8")
    payload = jwt.decode(encoded_token, 'fe155688cf6e4245a46b0cc4bdd4c56b', algorithms=['HS256'])
    event = payload['eventName']
    print(payload)
    if event == 'Webhook_Subscription':
        event_object = payload['eventArgs']['object']
        customer_id = payload['eventArgs']['entry'][0]['uuid']
        customer_resource_url = payload['eventArgs']['resource_url']
        #token = payload['auth']['accessToken'] No longer supported
        if event_object == 'COMPANY':
            client = Client(client_uuid=customer_id, resource_url=customer_resource_url)
            name = process_client(customer_resource_url)['name']
            print(name)
            client.name = name
            client.save()
            print("Client saved")
            return HttpResponse("Client saved")
        elif event_object == 'JOB':
            process_job(customer_resource_url)
            return JsonResponse({'Status':'Data saved'})
        elif event_object == 'TASK':
            process_task(customer_resource_url)
            return HttpResponse("OK")
    elif event == 'client_systems_event':
        try:
            systems = System.objects.filter(client__client_uuid=payload['eventArgs']['companyUUID'])
            rendered = render_to_string('sm8event/event.html', {'systems': systems})
            return JsonResponse({'eventResponse': rendered})
        except ObjectDoesNotExist:
            return JsonResponse({'eventResponse': 'No system(s) recorded for client.'})
    elif event == 'system_reports_event':
        total_jobs = Job.objects.filter(created__month=datetime.datetime.now().month).count()
        total_maintenance_jobs = Job.objects.filter(created__month=datetime.datetime.now().month).filter(job_category="Maintenance").count()
        total_clients_contract = System.objects.filter(date_created__month=datetime.datetime.now().month).filter(contracted="Y").count()
        total_clients_non_contract = System.objects.filter(date_created__month=datetime.datetime.now().month).filter(contracted="N").count()
        maintenance_hit_rate = (total_maintenance_jobs / total_jobs * 100) if total_jobs != 0 else 0
        access_control_audible = System.objects.filter(system_type="AC").filter(monitoring_type="A").count()
        access_control_monitored = System.objects.filter(system_type="AC").filter(monitoring_type="M").count()
        access_control_dualcom = System.objects.filter(system_type="AC").filter(monitoring_type="D").count()
        access_control_digi = System.objects.filter(system_type="AC").filter(monitoring_type="DI").count()
        access_control_digi_plus = System.objects.filter(system_type="AC").filter(monitoring_type="DIP").count()
        access_control_digi_air = System.objects.filter(system_type="AC").filter(monitoring_type="DIA").count()
        access_control_redcare_classic = System.objects.filter(system_type="AC").filter(monitoring_type="RC").count()
        access_control_redcare_secure = System.objects.filter(system_type="AC").filter(monitoring_type="RS").count()
        access_control_none = System.objects.filter(system_type="AC").filter(monitoring_type="N").count()
        access_control_total = access_control_audible + access_control_monitored + access_control_dualcom + access_control_digi + access_control_digi_plus + access_control_digi_air + access_control_redcare_classic + access_control_redcare_secure + access_control_none
        alarm_audible = System.objects.filter(system_type="AL").filter(monitoring_type="A").count()
        alarm_monitored = System.objects.filter(system_type="AL").filter(monitoring_type="M").count()
        alarm_dualcom = System.objects.filter(system_type="AL").filter(monitoring_type="D").count()
        alarm_digi = System.objects.filter(system_type="AL").filter(monitoring_type="DI").count()
        alarm_digi_plus = System.objects.filter(system_type="AL").filter(monitoring_type="DIP").count()
        alarm_digi_air = System.objects.filter(system_type="AL").filter(monitoring_type="DIA").count()
        alarm_redcare_classic = System.objects.filter(system_type="AL").filter(monitoring_type="RC").count()
        alarm_redcare_secure = System.objects.filter(system_type="AL").filter(monitoring_type="RS").count()
        alarm_none = System.objects.filter(system_type="AL").filter(monitoring_type="N").count()
        alarm_total = alarm_audible + alarm_monitored + alarm_dualcom + alarm_digi + alarm_digi_plus + alarm_digi_air + alarm_redcare_classic + alarm_redcare_secure + alarm_none
        cctv_audible = System.objects.filter(system_type="CT").filter(monitoring_type="A").count()
        cctv_monitored = System.objects.filter(system_type="CT").filter(monitoring_type="M").count()
        cctv_dualcom = System.objects.filter(system_type="CT").filter(monitoring_type="D").count()
        cctv_digi = System.objects.filter(system_type="CT").filter(monitoring_type="DI").count()
        cctv_digi_plus = System.objects.filter(system_type="CT").filter(monitoring_type="DIP").count()
        cctv_digi_air = System.objects.filter(system_type="CT").filter(monitoring_type="DIA").count()
        cctv_redcare_classic = System.objects.filter(system_type="CT").filter(monitoring_type="RC").count()
        cctv_redcare_secure = System.objects.filter(system_type="CT").filter(monitoring_type="RS").count()
        cctv_none = System.objects.filter(system_type="CT").filter(monitoring_type="N").count()
        cctv_total = cctv_audible + cctv_monitored + cctv_dualcom + cctv_digi + cctv_digi_plus + cctv_digi_air + cctv_redcare_classic + cctv_redcare_secure + cctv_none
        door_entry_audible = System.objects.filter(system_type="DE").filter(monitoring_type="A").count()
        door_entry_monitored = System.objects.filter(system_type="DE").filter(monitoring_type="M").count()
        door_entry_dualcom = System.objects.filter(system_type="DE").filter(monitoring_type="D").count()
        door_entry_digi = System.objects.filter(system_type="DE").filter(monitoring_type="DI").count()
        door_entry_digi_plus = System.objects.filter(system_type="DE").filter(monitoring_type="DIP").count()
        door_entry_digi_air = System.objects.filter(system_type="DE").filter(monitoring_type="DIA").count()
        door_entry_redcare_classic = System.objects.filter(system_type="DE").filter(monitoring_type="RC").count()
        door_entry_redcare_secure = System.objects.filter(system_type="DE").filter(monitoring_type="RS").count()
        door_entry_none = System.objects.filter(system_type="DE").filter(monitoring_type="N").count()
        door_entry_total = door_entry_audible + door_entry_monitored + door_entry_dualcom + door_entry_digi + door_entry_digi_plus + door_entry_digi_air + door_entry_redcare_classic + door_entry_redcare_secure + door_entry_none
        emergency_lights_audible = System.objects.filter(system_type="EL").filter(monitoring_type="A").count()
        emergency_lights_monitored = System.objects.filter(system_type="EL").filter(monitoring_type="M").count()
        emergency_lights_dualcom = System.objects.filter(system_type="EL").filter(monitoring_type="D").count()
        emergency_lights_digi = System.objects.filter(system_type="EL").filter(monitoring_type="DI").count()
        emergency_lights_digi_plus = System.objects.filter(system_type="EL").filter(monitoring_type="DIP").count()
        emergency_lights_digi_air = System.objects.filter(system_type="EL").filter(monitoring_type="DIA").count()
        emergency_lights_redcare_classic = System.objects.filter(system_type="EL").filter(monitoring_type="RC").count()
        emergency_lights_redcare_secure = System.objects.filter(system_type="EL").filter(monitoring_type="RS").count()
        emergency_lights_none = System.objects.filter(system_type="EL").filter(monitoring_type="N").count()
        emergency_lights_total = emergency_lights_audible + emergency_lights_monitored + emergency_lights_dualcom + emergency_lights_digi + emergency_lights_digi_plus + emergency_lights_digi_air + emergency_lights_redcare_classic + emergency_lights_redcare_secure + emergency_lights_none
        fire_alarm_audible = System.objects.filter(system_type="FA").filter(monitoring_type="A").count()
        fire_alarm_monitored = System.objects.filter(system_type="FA").filter(monitoring_type="M").count()
        fire_alarm_dualcom = System.objects.filter(system_type="FA").filter(monitoring_type="D").count()
        fire_alarm_digi = System.objects.filter(system_type="FA").filter(monitoring_type="DI").count()
        fire_alarm_digi_plus = System.objects.filter(system_type="FA").filter(monitoring_type="DIP").count()
        fire_alarm_digi_air = System.objects.filter(system_type="FA").filter(monitoring_type="DIA").count()
        fire_alarm_redcare_classic = System.objects.filter(system_type="FA").filter(monitoring_type="RC").count()
        fire_alarm_redcare_secure = System.objects.filter(system_type="FA").filter(monitoring_type="RS").count()
        fire_alarm_none = System.objects.filter(system_type="FA").filter(monitoring_type="N").count()
        fire_alarm_total = fire_alarm_audible + fire_alarm_monitored + fire_alarm_dualcom + fire_alarm_digi + fire_alarm_digi_plus + fire_alarm_digi_air + fire_alarm_redcare_classic + fire_alarm_redcare_secure + fire_alarm_none
        fire_extinguisher_audible = System.objects.filter(system_type="FE").filter(monitoring_type="A").count()
        fire_extinguisher_monitored = System.objects.filter(system_type="FE").filter(monitoring_type="M").count()
        fire_extinguisher_dualcom = System.objects.filter(system_type="FE").filter(monitoring_type="D").count()
        fire_extinguisher_digi = System.objects.filter(system_type="FE").filter(monitoring_type="DI").count()
        fire_extinguisher_digi_plus = System.objects.filter(system_type="FE").filter(monitoring_type="DIP").count()
        fire_extinguisher_digi_air = System.objects.filter(system_type="FE").filter(monitoring_type="DIA").count()
        fire_extinguisher_redcare_classic = System.objects.filter(system_type="FE").filter(monitoring_type="RC").count()
        fire_extinguisher_redcare_secure = System.objects.filter(system_type="FE").filter(monitoring_type="RS").count()
        fire_extinguisher_none = System.objects.filter(system_type="FE").filter(monitoring_type="N").count()
        fire_extinguisher_total = fire_extinguisher_audible + fire_extinguisher_monitored + fire_extinguisher_dualcom + fire_extinguisher_digi + fire_extinguisher_digi_plus + fire_extinguisher_digi_air + fire_extinguisher_redcare_classic + fire_extinguisher_redcare_secure + fire_extinguisher_none
        key_holding_audible = System.objects.filter(system_type="KE").filter(monitoring_type="A").count()
        key_holding_monitored = System.objects.filter(system_type="KE").filter(monitoring_type="M").count()
        key_holding_dualcom = System.objects.filter(system_type="KE").filter(monitoring_type="D").count()
        key_holding_digi = System.objects.filter(system_type="KE").filter(monitoring_type="DI").count()
        key_holding_digi_plus = System.objects.filter(system_type="KE").filter(monitoring_type="DIP").count()
        key_holding_digi_air = System.objects.filter(system_type="KE").filter(monitoring_type="DIA").count()
        key_holding_redcare_classic = System.objects.filter(system_type="KE").filter(monitoring_type="RC").count()
        key_holding_redcare_secure = System.objects.filter(system_type="KE").filter(monitoring_type="RS").count()
        key_holding_none = System.objects.filter(system_type="KE").filter(monitoring_type="N").count()
        key_holding_total = key_holding_audible + key_holding_monitored + key_holding_dualcom + key_holding_digi + key_holding_digi_plus + key_holding_digi_air + key_holding_redcare_classic + key_holding_redcare_secure + key_holding_none
        nurse_call_audible = System.objects.filter(system_type="NC").filter(monitoring_type="A").count()
        nurse_call_monitored = System.objects.filter(system_type="NC").filter(monitoring_type="M").count()
        nurse_call_dualcom = System.objects.filter(system_type="NC").filter(monitoring_type="D").count()
        nurse_call_digi = System.objects.filter(system_type="NC").filter(monitoring_type="DI").count()
        nurse_call_digi_plus = System.objects.filter(system_type="NC").filter(monitoring_type="DIP").count()
        nurse_call_digi_air = System.objects.filter(system_type="NC").filter(monitoring_type="DIA").count()
        nurse_call_redcare_classic = System.objects.filter(system_type="NC").filter(monitoring_type="RC").count()
        nurse_call_redcare_secure = System.objects.filter(system_type="NC").filter(monitoring_type="RS").count()
        nurse_call_none = System.objects.filter(system_type="NC").filter(monitoring_type="N").count()
        nurse_call_total = nurse_call_audible + nurse_call_monitored + nurse_call_dualcom + nurse_call_digi + nurse_call_digi_plus + nurse_call_digi_air + nurse_call_redcare_classic + nurse_call_redcare_secure + nurse_call_none
        refuge_audible = System.objects.filter(system_type="R").filter(monitoring_type="A").count()
        refuge_monitored = System.objects.filter(system_type="R").filter(monitoring_type="M").count()
        refuge_dualcom = System.objects.filter(system_type="R").filter(monitoring_type="D").count()
        refuge_digi = System.objects.filter(system_type="R").filter(monitoring_type="DI").count()
        refuge_digi_plus = System.objects.filter(system_type="R").filter(monitoring_type="DIP").count()
        refuge_digi_air = System.objects.filter(system_type="R").filter(monitoring_type="DIA").count()
        refuge_redcare_classic = System.objects.filter(system_type="R").filter(monitoring_type="RC").count()
        refuge_redcare_secure = System.objects.filter(system_type="R").filter(monitoring_type="RS").count()
        refuge_none = System.objects.filter(system_type="R").filter(monitoring_type="N").count()
        refuge_total = refuge_audible + refuge_monitored + refuge_dualcom + refuge_digi_plus + refuge_digi_air + refuge_redcare_classic + refuge_redcare_secure + refuge_none
        misc_audible = System.objects.filter(system_type="M").filter(monitoring_type="A").count()
        misc_monitored = System.objects.filter(system_type="M").filter(monitoring_type="M").count()
        misc_dualcom = System.objects.filter(system_type="M").filter(monitoring_type="D").count()
        misc_digi = System.objects.filter(system_type="M").filter(monitoring_type="DI").count()
        misc_digi_plus = System.objects.filter(system_type="M").filter(monitoring_type="DIP").count()
        misc_digi_air = System.objects.filter(system_type="M").filter(monitoring_type="DIA").count()
        misc_redcare_classic = System.objects.filter(system_type="M").filter(monitoring_type="RC").count()
        misc_redcare_secure = System.objects.filter(system_type="M").filter(monitoring_type="RS").count()
        misc_none = System.objects.filter(system_type="M").filter(monitoring_type="N").count()
        misc_total = misc_audible + misc_monitored + misc_dualcom + misc_digi + misc_digi_plus + misc_digi_air + misc_redcare_classic + misc_redcare_secure + misc_none
        response_time = Task.objects.aggregate(Avg('job_task_time_difference'), Max('job_task_time_difference'), Min('job_task_time_difference'))
        print(response_time)
        rendered = render_to_string(
            'sm8event/report.html',
            {
                'total_jobs':total_jobs,
                'total_maintenance_jobs':total_maintenance_jobs,
                'total_clients_contract':total_clients_contract,
                'total_clients_non_contract':total_clients_non_contract,
                'maintenance_hit_rate':maintenance_hit_rate,
                'access_control_audible':access_control_audible,
                'access_control_monitored':access_control_monitored,
                'access_control_dualcom':access_control_dualcom,
                'access_control_digi':access_control_digi,
                'access_control_digi_plus':access_control_digi_plus,
                'access_control_digi_air':access_control_digi_air,
                'access_control_redcare_classic':access_control_redcare_classic,
                'access_control_redcare_secure':access_control_redcare_secure,
                'access_control_none':access_control_none,
                'access_control_total':access_control_total,
                'alarm_monitored':alarm_monitored,
                'alarm_audible':alarm_audible,
                'alarm_dualcom':alarm_dualcom,
                'alarm_digi':alarm_digi,
                'alarm_digi_plus':alarm_digi_plus,
                'alarm_digi_air':alarm_digi_air,
                'alarm_redcare_classic':alarm_redcare_classic,
                'alarm_redcare_secure':alarm_redcare_secure,
                'alarm_none':alarm_none,
                'alarm_total':alarm_total,
                'cctv_monitored':cctv_monitored,
                'cctv_audible':cctv_audible,
                'cctv_dualcom':cctv_dualcom,
                'cctv_digi':cctv_digi,
                'cctv_digi_plus':cctv_digi_plus,
                'cctv_digi_air':cctv_digi_air,
                'cctv_redcare_classic':cctv_redcare_classic,
                'cctv_redcare_secure':cctv_redcare_secure,
                'cctv_none':cctv_none,
                'cctv_total':cctv_total,
                'door_entry_audible':door_entry_audible,
                'door_entry_monitored':door_entry_monitored,
                'door_entry_dualcom':door_entry_dualcom,
                'door_entry_digi':door_entry_digi,
                'door_entry_digi_plus':door_entry_digi_plus,
                'door_entry_digi_air':door_entry_digi_air,
                'door_entry_redcare_classic':door_entry_redcare_classic,
                'door_entry_redcare_secure':door_entry_redcare_secure,
                'door_entry_none':door_entry_none,
                'door_entry_total':door_entry_total,
                'emergency_lights_audible':emergency_lights_audible,
                'emergency_lights_monitored':emergency_lights_monitored,
                'emergency_lights_dualcom':emergency_lights_dualcom,
                'emergency_lights_digi':emergency_lights_digi,
                'emergency_lights_digi_plus':emergency_lights_digi_plus,
                'emergency_lights_digi_air':emergency_lights_digi_air,
                'emergency_lights_redcare_classic':emergency_lights_redcare_classic,
                'emergency_lights_redcare_secure':emergency_lights_redcare_secure,
                'emergency_lights_none':emergency_lights_none,
                'emergency_lights_total':emergency_lights_total,
                'fire_alarm_audible':fire_alarm_audible,
                'fire_alarm_monitored':fire_alarm_monitored,
                'fire_alarm_dualcom':fire_alarm_dualcom,
                'fire_alarm_digi':fire_alarm_digi,
                'fire_alarm_digi_plus':fire_alarm_digi_plus,
                'fire_alarm_digi_air':fire_alarm_digi_air,
                'fire_alarm_redcare_classic':fire_alarm_redcare_classic,
                'fire_alarm_redcare_secure':fire_alarm_redcare_secure,
                'fire_alarm_none':fire_alarm_none,
                'fire_alarm_total':fire_alarm_total,
                'fire_extinguisher_audible':fire_extinguisher_audible,
                'fire_extinguisher_monitored':fire_extinguisher_monitored,
                'fire_extinguisher_dualcom':fire_extinguisher_dualcom,
                'fire_extinguisher_digi':fire_extinguisher_digi,
                'fire_extinguisher_digi_plus':fire_extinguisher_digi_plus,
                'fire_extinguisher_digi_air':fire_extinguisher_digi_air,
                'fire_extinguisher_redcare_classic':fire_extinguisher_redcare_classic,
                'fire_extinguisher_redcare_secure':fire_extinguisher_redcare_secure,
                'fire_extinguisher_none':fire_extinguisher_none,
                'fire_extinguisher_total':fire_extinguisher_total,
                'key_holding_audible':key_holding_audible,
                'key_holding_monitored':key_holding_monitored,
                'key_holding_dualcom':key_holding_dualcom,
                'key_holding_digi':key_holding_digi,
                'key_holding_digi_plus':key_holding_digi_plus,
                'key_holding_digi_air':key_holding_digi_air,
                'key_holding_redcare_classic':key_holding_redcare_classic,
                'key_holding_redcare_secure':key_holding_redcare_secure,
                'key_holding_none':key_holding_none,
                'key_holding_total':key_holding_total,
                'nurse_call_audible':nurse_call_audible,
                'nurse_call_monitored':nurse_call_monitored,
                'nurse_call_dualcom':nurse_call_dualcom,
                'nurse_call_digi':nurse_call_digi,
                'nurse_call_digi_plus':nurse_call_digi_plus,
                'nurse_call_digi_air':nurse_call_digi_air,
                'nurse_call_redcare_classic':nurse_call_redcare_classic,
                'nurse_call_redcare_secure':nurse_call_redcare_secure,
                'nurse_call_none':nurse_call_none,
                'nurse_call_total':nurse_call_total,
                'refuge_audible':refuge_audible,
                'refuge_monitored':refuge_monitored,
                'refuge_dualcom':refuge_dualcom,
                'refuge_digi':refuge_digi,
                'refuge_digi_plus':refuge_digi_plus,
                'refuge_digi_air':refuge_digi_air,
                'refuge_redcare_classic':refuge_redcare_classic,
                'refuge_redcare_secure':refuge_redcare_secure,
                'refuge_none':refuge_none,
                'refuge_total':refuge_total,
                'misc_audible':misc_audible,
                'misc_monitored':misc_monitored,
                'misc_dualcom':misc_dualcom,
                'misc_digi':misc_digi,
                'misc_digi_plus':misc_digi_plus,
                'misc_digi_air':misc_digi_air,
                'misc_redcare_classic':misc_redcare_classic,
                'misc_redcare_secure':misc_redcare_secure,
                'misc_none':misc_none,
                'misc_total':misc_total,
                'response_time':response_time
            }
        )
        return JsonResponse({'eventResponse':rendered})
