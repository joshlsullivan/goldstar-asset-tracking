from django.shortcuts import render
from django.views.generic import FormView
from django.http import JsonResponse


from .system_forms import SystemForm
from .mixins import AjaxFormMixin

class SystemFormView(AjaxFormMixin, FormView):
    form_class = SystemForm
    template_name = 'system/form.html'
    success_url = '/form-success/'

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
