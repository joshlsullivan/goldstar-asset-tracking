from django.urls import path
from . import views

app_name = 'client'
urlpatterns = [
    path('system/', views.SystemFormView.as_view(), name='system'),
    path('system/<int:pk>/', views.SystemFormUpdateView.as_view(), name='system-update'),
    path('system/delete/<int:pk>/', views.SystemFormDeleteView.as_view(), name='system-delete'),
]
