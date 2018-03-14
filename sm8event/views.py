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
    r = requests.get(url, auth=auth)
    category = r.json()
    name = category['name']
    return name

def process_job(customer_resource_url):
    url = customer_resource_url
    #token=token
    #headers = {'Authorization':'Bearer {}'.format(token)}
    r = requests.get(url, auth=auth)
    job = r.json()
    client = Client.objects.get(client_uuid=job['company_uuid'])
    j = client.job_set.create(job_uuid=job['uuid'], job_category=process_category(job['category_uuid']))
    j = client.job_set.create(job_uuid=job['uuid'])
    print(j)
    return j

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
    url = customer_resource_url
    #headers = {'Authorization': 'Bearer {}'.format(token)}
    r = requests.get(url, auth=auth)
    client = r.json()
    print(client)
    return client

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
            c = Client(client_uuid=customer_id, resource_url=customer_resource_url)
            c.name = process_client(customer_resource_url)['name']
            c.save()
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
        maintenance_hit_rate = total_maintenance_jobs / total_jobs * 100
        access_control_audible = System.objects.filter(system_type="AC").filter(monitoring_type="A").count()
        access_control_monitored = System.objects.filter(system_type="AC").filter(monitoring_type="M").count()
        access_control_total = access_control_audible + access_control_monitored
        alarm_audible = System.objects.filter(system_type="AL").filter(monitoring_type="A").count()
        alarm_monitored = System.objects.filter(system_type="AL").filter(monitoring_type="M").count()
        alarm_total = alarm_audible + alarm_monitored
        cctv_audible = System.objects.filter(system_type="CT").filter(monitoring_type="A").count()
        cctv_monitored = System.objects.filter(system_type="CT").filter(monitoring_type="M").count()
        cctv_total = cctv_audible + cctv_monitored
        door_entry_audible = System.objects.filter(system_type="DE").filter(monitoring_type="A").count()
        door_entry_monitored = System.objects.filter(system_type="DE").filter(monitoring_type="M").count()
        door_entry_total = door_entry_audible + door_entry_monitored
        emergency_lights_audible = System.objects.filter(system_type="EL").filter(monitoring_type="A").count()
        emergency_lights_monitored = System.objects.filter(system_type="EL").filter(monitoring_type="M").count()
        emergency_lights_total = emergency_lights_audible + emergency_lights_monitored
        fire_alarm_audible = System.objects.filter(system_type="FA").filter(monitoring_type="A").count()
        fire_alarm_monitored = System.objects.filter(system_type="FA").filter(monitoring_type="M").count()
        fire_alarm_total = fire_alarm_audible + fire_alarm_monitored
        fire_extinguisher_audible = System.objects.filter(system_type="FE").filter(monitoring_type="A").count()
        fire_extinguisher_monitored = System.objects.filter(system_type="FE").filter(monitoring_type="M").count()
        fire_extinguisher_total = fire_extinguisher_audible + fire_extinguisher_monitored
        key_holding_audible = System.objects.filter(system_type="KE").filter(monitoring_type="A").count()
        key_holding_monitored = System.objects.filter(system_type="KE").filter(monitoring_type="M").count()
        key_holding_total = key_holding_audible + key_holding_monitored
        nurse_call_audible = System.objects.filter(system_type="NC").filter(monitoring_type="A").count()
        nurse_call_monitored = System.objects.filter(system_type="NC").filter(monitoring_type="M").count()
        nurse_call_total = nurse_call_audible + nurse_call_monitored
        refuge_audible = System.objects.filter(system_type="R").filter(monitoring_type="A").count()
        refuge_monitored = System.objects.filter(system_type="R").filter(monitoring_type="M").count()
        refuge_total = refuge_audible + refuge_monitored
        response_time = Task.objects.aggregate(Avg('job_task_time_difference'), Max('job_task_time_difference'), Min('job_task_time_difference'))
        print(response_time)
        rendered = render_to_string('sm8event/report.html', {'total_jobs':total_jobs, 'total_maintenance_jobs':total_maintenance_jobs, 'total_clients_contract':total_clients_contract, 'total_clients_non_contract':total_clients_non_contract, 'maintenance_hit_rate':maintenance_hit_rate, 'access_control_audible':access_control_audible, 'access_control_monitored':access_control_monitored, 'access_control_total':access_control_total, 'alarm_monitored':alarm_monitored, 'alarm_audible':alarm_audible, 'alarm_total':alarm_total, 'cctv_monitored':cctv_monitored, 'cctv_audible':cctv_audible, 'cctv_total':cctv_total, 'door_entry_audible':door_entry_audible, 'door_entry_monitored':door_entry_monitored, 'door_entry_total':door_entry_total, 'emergency_lights_audible':emergency_lights_audible, 'emergency_lights_monitored':emergency_lights_monitored, 'emergency_lights_total':emergency_lights_total, 'fire_alarm_audible':fire_alarm_audible, 'fire_alarm_monitored':fire_alarm_monitored, 'fire_alarm_total':fire_alarm_total, 'fire_extinguisher_audible':fire_extinguisher_audible, 'fire_extinguisher_monitored':fire_extinguisher_monitored, 'fire_extinguisher_total':fire_extinguisher_total, 'key_holding_audible':key_holding_audible, 'key_holding_monitored':key_holding_monitored, 'key_holding_total':key_holding_total, 'nurse_call_audible':nurse_call_audible, 'nurse_call_monitored':nurse_call_monitored, 'nurse_call_total':nurse_call_total, 'refuge_audible':refuge_audible, 'refuge_monitored':refuge_monitored, 'refuge_total':refuge_total, 'response_time':response_time})
        return JsonResponse({'eventResponse':rendered})
