from django.urls import path

from system.views import SystemListView

app_name = 'system'
urlpatterns = [
    path('', SystemListView.as_view(), name='system-list'),
    path('system/<monitoring_type>/', MonitoringTypeListView.as_view(), name='monitoring_type'),
]
