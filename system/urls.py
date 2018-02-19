from django.urls import path
from . import views

app_name = 'system'
urlpatterns = [
    path('', views.SystemFormView.as_view(), name='system'),
    path('<int:pk>/', views.SystemFormUpdateView.as_view(), name='system-update'),
]
