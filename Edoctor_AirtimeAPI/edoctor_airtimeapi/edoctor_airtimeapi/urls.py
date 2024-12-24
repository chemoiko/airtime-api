"""
URL configuration for edoctor_airtimeapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from apidashboard import views
import apidashboard.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('airtime/api/',include(('airtimeapi.urls','airtimeapi'),namespace='airtimeapi')),
    path('dashboard',include(('apidashboard.urls','apidashboard'),namespace='dashboardapi')),
    #path('',apidashboard.views.redirect),
    #path('verification/', include('verify_email.urls')),
    path(f'verification/user/verify-email/<useremail>/<usertoken>/', views.verify_user_and_activate, name='verify-email'),
    path(f'verification/user/verify-email/request-new-link/<useremail>/<usertoken>/', views.request_new_link, name='request-new-link-from-token'),
    path(f'verification/user/verify-email/request-new-link/', views.request_new_link, name='request-new-link-from-email'),
    
    #path('verification/', include('verify_email')),
    path('',include(('apidashboard.urls','apidashboard'),namespace='dashboardapi')),
    #path(r'^docs/', include('sphinxdoc.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
