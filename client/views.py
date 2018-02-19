from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy

from .system_forms import SystemForm
from .mixins import AjaxFormMixin

from client.models import System

class SystemFormView(AjaxFormMixin, FormView):
    form_class = SystemForm
    template_name = 'client/form.html'
    success_url = '/form-success/'

    def dispatch(self, *args, **kwargs):
        if 'oauth_token' in self.request.session:
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('/')

    def form_invalid(self, form):
        response = super(SystemFormView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(SystemFormView, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response

class SystemFormUpdateView(UpdateView):
    model = System
    fields = '__all__'
    template_name_suffix = '_update_form'

class SystemFormDeleteView(DeleteView):
    model = System
    success_url = 'https://warm-earth-88738.herokuapp.com/client/close/'

class SystemCloseWindow(TemplateView):
    template_name = 'client/close_window_success.html'
