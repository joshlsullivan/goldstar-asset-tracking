from django.urls import path

from system.views import SystemListView, MonitoringTypeListView, SystemTypeListView

app_name = 'system'
urlpatterns = [
    path('', SystemListView.as_view(), name='system-list'),
    path('monitoring/<monitoring_type>/', MonitoringTypeListView.as_view(), name='monitoring_type'),
    path('system/<system_type>/', SystemTypeListView.as_view(), name='system_type'),
]
