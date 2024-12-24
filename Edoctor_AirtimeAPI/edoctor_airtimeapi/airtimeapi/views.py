from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from django.contrib.auth.decorators import permission_required
from .serializers import TestSerializer
from .models import Data#, APIcredentials
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.http import urlencode
from .yo_api import YO_API
import json
from .logmodel import LogModel
import uuid,random,sys,traceback
from .airtime_auth import AirtimeAuthentication
from .restperms import APIperm
#from guardian.shortcuts import assign_perm
# Create your views here.

#yoapi = YO_API("1755147","13QT-GZI5-RKEA-3dU9-uz2S-Gcov-jWTF-7uq9")
yoapi = YO_API("90005702859","MsUl-Ei4O-BmJo-apHP-npHY-wsYT-c8nc-skny")
#yoapi = YO_API("90005702859","MsUl-Ei4O-BmJo-apHP-npHY-wsYT-c8nc-skny")
class AuthMan(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print("new data: ",request.data)
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        print("got user: ",user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'email':user.email
        })
@api_view(['GET'])

@authentication_classes([AirtimeAuthentication])

##@permission_classes([IsAuthenticated])
def getData(request):
    #datum = Data.objects.all()
    #serializer = TestSerializer(datum[0],many=False)
    #print(datum)
    #json_data = serializer.data
    #print(json_data)
    #rest_data = Response(json_data)
    xuser = request.user
    auser = xuser
    print(auser)
    #return render(request,'index.html')
    return Response({
        "message":"hello world"
    })
    #redirect(servePage)

@api_view(['GET'])
#@authentication_classes([AirtimeAuthentication])
##@permission_classes([IsAuthenticated])
def servePage(request):
    #datum = Data.objects.all()
    #serializer = TestSerializer(datum[0],many=False)
    #print(datum)
    #json_data = serializer.data
    #print(json_data)
    #rest_data = Response(json_data)
    auth_user = request.session.get("user")

    if auth_user==None:
        is_authenticated = False
    else:
        is_authenticated = True
    print("authenticated: ",is_authenticated)
    try:
        if(is_authenticated==True):
            url_name = request.path
            file_name = url_name.split('/')[-1]
            print("Using url: ", file_name)
            xuser = request.user
            auser = xuser
            print(auser)
            return render(request,file_name)
        else:
            return render(request,"page-login.html")
    except:
        return render(request,"page-login.html")

@api_view(['POST'])
def auth(request):
    data = request.data

@api_view(['POST'])
def register(request):
    """
    Register a new user.

    Registers a new user with the given request data.

    Args:
        request (Request): The request object containing the user registration data.

    Returns:
        A response object indicating the success or failure of the registration with the returned username and token

    Raises:
        ValueError: If the request object is missing any required data.
    """
    requester = request.data
    
    user_name = requester['username']
    email = requester['email']
    password = requester['password']
    name_dic = {}
    user = request.user
    #User.objects.get(username=user_name, password=password)
    print("\n\tlogin data: ",user)
    email_exists = (len(User.objects.filter(email=email))==0)
    username_exists = (len(User.objects.filter(username=user_name))==0)
    print(f"username {user_name} status: {username_exists}")
    print(f"email {email} status: {email_exists}")

    valid_object = [
        {"type":"email","valid":email_exists},
        {"type":"username","valid":username_exists},
        {"type":"password","valid":True}

    ]
    
    if user.is_anonymous is True:
        try:
            if((email_exists==False) or (username_exists==False)):
                response_dic = {'status_code':404, 'data':valid_object,'message':'user error, email already exists'}
                return Response(response_dic)
            user_x = User(username=user_name,email=email,password=password)
            
            user_x.save()
            token,created=Token.objects.get_or_create(user=user_x)
            print(created)
            name_dic = {'status_code':200,'name':user_x.get_username(),'token':token.key}
            return Response(name_dic)
        except:
            name_dic = {'status_code':500,'message':'user error, email or username exists'}
            return Response(name_dic)
    else:
        token,created=Token.objects.get_or_create(user=user)
        print("\n\tcreated user: ",created)
        name_dic = {'name':user.get_username(),'token':token.key}
        return Response(name_dic)

@api_view(['POST'])
def notify(request):
    url_encode_msg = urlencode({"narrative":"Transaction Received Please"})
    return HttpResponse(url_encode_msg)
@api_view(['POST'])
def login(request):
    """
    login a new user.

    login a user with the given request data.

    Args:
        request (Request): The request object containing the user registration data.

    Returns:
        A response object indicating the success or failure of the registration with the returned username and token

    Raises:
        ValueError: If the request object is missing any required data.
    """
    requester = request.data
    print("request form is: ", requester)
    #user_name = requester['username']
    # password = requester['password']
    
    user_name = request.POST.get('email','')
    password = request.POST.get('password','')
    name_dic = {}
    #uers_up = User.objects.exists(username=user_name,password=password)
    print("username: ",user_name)
    print('password : ',password )
    is_authen = request.user
    print("is authenticated: ",is_authen.username)
    try: 
        #user = authenticate(username=user_name, password=password)
        user = User.objects.get(username=user_name, password=password)
        
        print("user: ",user)
        if user is not None:
            login(request, user)
            request.session['user'] = user
        else:
           
            print("user status: ",xuser)
            return  render(request,"page-login.html")
        #user = User.objects.get(username=user_name, password=password)
        
       # token,created=Token.objects.get_or_create(user=user)
        #print("\n\tcreated user: ",created)
        #name_dic = {'status_code':200,'message':'user success','name':user.get_username(),'token':token.key}
        #return Response(name_dic)
        return render(request,"index.html")
    except Exception:
        print("user error")
        traceback.print_exc()
        #return render(request,"index.html")
        return Response({"status_code":500,"message":"User error"})



@api_view(['POST'])
def check_balance(request):
    pass

@api_view(['POST'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated])
def sendAirtime(request):
    """
    Send airtime to a specified phone number.

    This view is responsible for processing POST requests to send airtime to a phone number.

    Parameters:
    request (HttpRequest): The incoming HTTP request, containing json request in the format:
    {
      "telno":"256700000000",
      "amount":15060
    }
    Returns:
    Response: A JSON response containing the result of the airtime transaction.
    """
    #256700000000
    #json_request = json.loads(request.body)
    #msisdn = json_request["telno"]
    #amount = json_request["amount"]
    yoapi_response = yoapi.sendAirtime(request)

    return Response(yoapi_response)

@api_view(['GET'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated])
def getInfo(request):
    """
    Retrieve information for a given phone number.

    This view is responsible for processing POST requests to retrieve information for a phone number.

    Parameters:
    request (HttpRequest): The incoming HTTP request. containing json request in the format:
    {
      "telno":"256700000000"
    }

    Returns:
    Response: A JSON response containing the information for the given phone number.
    """
    #json_request = json.loads(request.body)
    #msisdn = json_request["telno"]
    yoapi_response = yoapi.getMSISDNInfo(request)
    return Response(yoapi_response)

@api_view(['POST'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated])
def buyAirtime(request):
    """
    Buy airtime for a specified phone number.

    This view is responsible for processing POST requests to buy airtime for a phone number.

    Parameters:
    request (HttpRequest): The incoming HTTP request, containing json request in the format:
    {
      "provider":"mtn",
      "amount":15060
    }

    provider can be any of the following: mtn, MTN , airtel, AIRTEL, utl, UTL.

    Returns:
    Response: A JSON response containing the result of the airtime purchase.
    """
    #256700000000
    #json_request = json.loads(request.body)
    #netwrk = json_request["provider"]
    #amount = json_request["amount"]
    yoapi_response = yoapi.buyAirtime(request)
    return Response(yoapi_response)

@api_view(['POST'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated])
def depositFunds(request):
    """
    Deposit funds into the user's account.

    This view is responsible for processing POST requests to deposit funds into the user's account.

    Parameters:
    request (HttpRequest): The incoming HTTP request, containing json request in the format:
    {
      "telno":"256700000000",
      "amount":15060
    }

    Returns:
    Response: A JSON response containing the result of the funds deposit.
    """

    #256700000000
    #json_request = json.loads(request.body)
    #telno = json_request["telno"]
    #amount = json_request["amount"]
    yoapi_response = yoapi.depositMoney(request)
    return Response(yoapi_response)

@api_view(['POST'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated])
def withdrawFunds(request):
    """
    Withdraw funds from the user's account.

    This view is responsible for processing POST requests to withdraw funds from the user's account.

    Parameters:
    request (HttpRequest): The incoming HTTP request, containing json request in the format:
    {
      "telno":"256700000000",
      "amount":15060
    }

    Returns:
    Response: A JSON response containing the result of the funds withdrawal.
    """
    #256700000000
    json_request = json.loads(request.body)
    telno = json_request["telno"]
    amount = json_request["amount"]
    yoapi_response = yoapi.withdrawMoney(request)
    return Response(yoapi_response)

@api_view(['POST'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated]) 
def submitBankDeposit(request):
    request_user = request.user.get_username()
    
    #json_request = json.loads(request.body)
    print(request_user)
    yoapi_response = yoapi.submitBankDeposit(request_user,request)
    return Response(yoapi_response)

@api_view(['POST'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated]) 
def makeInternalTransfer(request):
    request_user = request.user.get_username()
    
    #json_request = json.loads(request.body)
    #print(request_user)
    yoapi_response = yoapi.makeInternalTransfer(request)
    return Response(yoapi_response)

@api_view(['POST'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated]) 
def withdrawMoneyToBank(request):
    print("withdrawing money to bank")
    """## _summary_

    ### Args:
        - `request (_type_)`: _description_

    ### Returns:
        - `_type_`: _description_
    """
    #json_request = json.loads(request.body)
    yoapi_response = yoapi.withdrawMoneyToBank(request)
    return Response(yoapi_response)

@api_view(['GET'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated]) 
def getTransactionStatus(request):
    """## _summary_

    ### Args:
        - `request (_type_)`: _description_

    ### Returns:
        - `_type_`: _description_
    """
    json_request = json.loads(request.body)
    yoapi_response = yoapi.checkTransactionStatus(request)
    return Response(yoapi_response)


@api_view(['GET'])
@authentication_classes([AirtimeAuthentication])
##@permission_classes([IsAuthenticated]) 
def getLogs(request):
    """## _summary_

    ### Args:
        - `request (_type_)`: _description_

    ### Returns:
        - `_type_`: _description_
    """
    #json_request = json.loads(request.body)
    #log_type = json_request["category"]
    print("airtime log on")
    request_user = request.user
    print("\n\t using request user: ",request_user)
    draw_id = item_no = request.GET.get('draw')
    log_type = request.GET.get('type')
    item_index = request.GET.get('start')
    item_no = request.GET.get('length')
    print(f"data table is: {log_type} {item_index} and total: {item_no} with draw id: {draw_id}")
    alogmodel = LogModel(request.user)
    #log_columns, 
    log_data = alogmodel.getLog(log_type)
    print(f"\n\n\t\ttotal rows: {len(log_data)}\n\n")

    more_records = log_data[int(item_index): (int(item_index)+1)+int(item_no)]
    print(more_records)
    #"columns":log_columns,
    log_response = {
        "draw":draw_id,
        "recordsTotal":len(log_data),
        "recordsFiltered": len(log_data),
        "data": more_records
    }
    return Response(log_response)

@api_view(['GET'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated]) 
def getBankWithdrawStatus(request):
    """## _summary_

    ### Args:
        - `request (_type_)`: _description_

    ### Returns:
        - `_type_`: _description_
    """
    #json_request = json.loads(request.body)
    yoapi_response = yoapi.getBankWithdrawStatus(request)
    return Response(yoapi_response)

@api_view(['GET'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated]) 
def getBalance(request):
    """## _summary_

    ### Args:
        - `request (_type_)`: _description_

    ### Returns:
        - `_type_`: _description_
    """
    
    yoapi_response = yoapi.checkBalance(request)
    return Response(yoapi_response)

@api_view(['GET'])
@authentication_classes([AirtimeAuthentication])
#@permission_classes([IsAuthenticated]) 
def getMiniStatement(request):
    """## _summary_

    ### Args:
        - `request (_type_)`: _description_

    ### Returns:
        - `_type_`: _description_
    """
    #json_request = json.loads(request.body)
    yoapi_response = yoapi.getMiniStatement(request)
    return Response(yoapi_response)


# Generate api credentials
@api_view(['POST'])
@authentication_classes([AirtimeAuthentication])
##@permission_classes([IsAuthenticated])
def generateAPICredentials(request):
    get_params = request.body
    print("request params are: ",get_params)
    username = random.randint(0,sys.maxsize)
    user_x = User(username=username)
    user_x.is_active = False
    user_x.save()
    token=Token.objects.create(user=user_x)
    passwd = uuid.uuid4().hex

    #apicredentials = APIcredentials(owner = request.user,token_username = username, token = token)
    # apicredentials.save()
    print("username is: ",username)
    print("password is: ",passwd)
    return Response({"status_code":200,"data":{"api_username":username,"api_password":passwd}})