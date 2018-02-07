from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from urllib.parse import parse_qs
import json
import requests

from client.models import Client

@csrf_exempt
def webhook(request):
    body = request.body
    data = parse_qs(body, encoding='utf-8', keep_blank_values=True)
    challenge = request.POST.get('challenge', '')
    mode = request.POST.get('mode', '')
    payload = json.loads(body.decode('utf-8'))
    webhook_uuid = payload['entry'][0]['uuid']
    resource_url = payload['resource_url']
    webhook_object = payload['object']
    if challenge and mode == 'subscribe':
        return HttpResponse("{}".format(challenge))
    elif webhook_object == 'COMPANY':
        print(payload)
        obj, created = Client.objects.get_or_create(
            client_uuid = webhook_uuid,
            defaults = {
                'resource_url': resource_url,
            }
        )
        return HttpResponse("Client created")
