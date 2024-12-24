from django.urls import path,re_path
from . import views

from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [  
    path('post/', views.getData),
    path('', views.getData),
    #path('dashboard/*', views.servePage),
    #re_path(r'^dashboard/.*$',views.servePage),
    #path('auth/register',views.register), #registration api endpoint
    #path('auth/login',views.login), #registration api endpoint
    path('send_airtime',views.sendAirtime), #send airtime endpoint
    path('telno_info',views.getInfo), #get telephone number infomation endpoint
    path('buy_airtime',views.buyAirtime), #buy airtime api endpoint
    path('deposit',views.depositFunds), #deposit money api endpoint
    path('withdraw',views.withdrawFunds),#withdraw money endpoint
    path('auth/token',obtain_auth_token, name='api_token_auth'), #authorization endpoint
    path('auth/login',views.AuthMan.as_view()), #not applicable
    path('bankdeposit',views.submitBankDeposit),#submit bank deposit request endpoint
    path('internal_funds_transfer',views.makeInternalTransfer), #internal funds transfer endpoint
    path('mini_statement',views.getMiniStatement),
    path('balance',views.getBalance),
    path('withdraw_status',views.getBankWithdrawStatus),
    path('transaction_status',views.getTransactionStatus),
    path("withdraw_to_bank", views.withdrawMoneyToBank),
    path("notify",views.notify),
    path("logs",views.getLogs,name="getLogs"),
    path("generate_apikey",views.generateAPICredentials)
]