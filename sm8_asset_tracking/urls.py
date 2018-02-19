"""sm8_asset_tracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from sm8auth.views import AuthView, CallbackView
from webhook import views as webhook_views
from sm8event import views as event_views

urlpatterns = [
    path('', AuthView.as_view(), name='auth'),
    path('asset_tracking_event/', event_views.asset_tracking_event, name='event'),
    path('callback/', CallbackView.as_view(), name='callback'),
    path('webhook/', webhook_views.webhook, name='webhook'),
    path('system/', include('system.urls'),
    path('admin/', admin.site.urls),
]
