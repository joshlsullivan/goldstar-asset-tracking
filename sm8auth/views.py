from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from requests_oauthlib import OAuth2Session
import requests

client_id = '860242'
client_secret = 'fe155688cf6e4245a46b0cc4bdd4c56b'
authorization_base_url = 'https://go.servicem8.com/oauth/authorize'
token_url = 'https://go.servicem8.com/oauth/access_token'
redirect_uri = 'https://warm-earth-88738.herokuapp.com/callback'
scope = [
    'manage_customers'
]

def subscribe(access_token):
    url = "https://api.servicem8.com/webhook_subscriptions"
    payload = {'object':'company','fields':'uuid','callback_url':'https://warm-earth-88738.herokuapp.com/webhook/'}
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    r = requests.post(url, data=payload, headers=headers)
    print(r.content)

def unsubscribe(access_token):
    url = "https://api.servicem8.com/webhook_subscriptions"
    payload = "object=company"
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    r = requests.delete(url, data=payload, headers=headers)
    print(r.content)

class AuthView(View):
    def get(self, request):
        servicem8 = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
        authorization_url, state = servicem8.authorization_url(authorization_base_url)
        request.session['oauth_state'] = state
        print(authorization_url)
        return redirect(authorization_url)

class CallbackView(View):
    def get(self, request):
        servicem8 = OAuth2Session(client_id, redirect_uri=redirect_uri, state=request.session['oauth_state'])
        token = servicem8.fetch_token(token_url, client_secret=client_secret, code=request.GET.get('code', None))
        request.session['oauth_token'] = token
        access_token = token['access_token']
        print(access_token)
        #subscribe(access_token)
        #unsubscribe(access_token)
        return redirect('https://go.servicem8.com')
