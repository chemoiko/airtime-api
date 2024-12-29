from django.urls import path, re_path
from . import views
from django.conf import settings


urlpatterns = [
    path('auth/register', views.register),  # Registration API endpoint
    path('auth/login', views.loginUser),    # Login API endpoint
    path('auth/logout', views.logoutUser),
    path('login', views.loginView),
    path('', views.redirectUser, name="redirect"),  # Root path
    path('dashboard', views.dashboard),  # Updated path for the dashboard
    path('add_admin', views.addAdmin),
    re_path(r'^.*html', views.dashboard),  # Regex for matching HTML files
    path('apikey/generate_apikey', views.generateAPICredentials),
    path('logs', views.getLogs),
    path('requestDocVerification', views.requestVerifyDocs),
    path('verifyCompany', views.verifyDoc),
    path('getDoc', views.getVerificationDoc),
    path('getDocs', views.getVerificationDocs),
    path('verifyKey', views.verifyKey),
    path('disableKey', views.disableKey),
    path('public/TC', views.getPublic),
    path('public/services', views.getPublic),
    path('public/faq', views.getPublic),
    path('public/aboutus', views.getPublic),
    path('public/contactus', views.getPublic),
    path('public/privacy', views.getPublic),
    # path('', views.redirect)

]
