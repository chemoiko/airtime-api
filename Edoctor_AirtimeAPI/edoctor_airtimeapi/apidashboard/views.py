from django.shortcuts import render, redirect
# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from django import forms
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required, login_required
# from .models import Data
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import Permission
from django.utils.http import urlencode
import traceback
import json
import uuid
from django.contrib.auth import logout, login
from .models import APIcredentials, DashboardUsers, Companies, Uploaded_File
from .consts import dashboard_constants
import uuid
import random
import sys
from .logmodel import Logs
from django.template import RequestContext, loader

import zipfile36 as zipfile
import os
from edoctor_airtimeapi import settings
import time
import logging
# from verify_email.email_handler import send_verification_email, _VerifyEmail
from .forms.UserForms import NewUserForm
from .emailverify import EdocVerify
from .verify_views import *
# from . import ziputils
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])


def servePage(request):
    # datum = Data.objects.all()
    # serializer = TestSerializer(datum[0],many=False)
    # print(datum)
    # json_data = serializer.data
    # print(json_data)
    # rest_data = Response(json_data)
    auth_user = request.session.get("user")

    if auth_user == None:
        is_authenticated = False
    else:
        is_authenticated = True
    print("authenticated: ", is_authenticated)
    try:
        if (is_authenticated == True):
            url_name = request.path
            file_name = url_name.split('/')[-1]
            print("Using url: ", file_name)
            xuser = request.user
            auser = xuser
            print(auser)
            return render(request, file_name)
        else:
            return render(request, "page-login.html")
    except:
        return render(request, "page-login.html")


def xregister(request):
    return render(request, "page-register.html")


@api_view(['POST', 'GET'])
@csrf_exempt
def register(request):
    """
    Register a new dashboard user.

    Registers a new user with the given request data.

    Args:
        request (Request): The request object containing the user registration data.

    Returns:
        A response object indicating the success or failure of the registration with the returned username and token

    Raises:
        ValueError: If the request object is missing any required data.
    """
    if request.method == "GET":
        print("using register get")
        return render(request, "page-register.html")

    requester = request.data
    user_role = requester["role"]
    fullnames = str(requester['fullnames']).split(' ')
    print("fullnames are: ", fullnames)
    user_name = requester['username']
    email = requester['email']
    password = requester['password']
    user_role = requester["role"]
    name_dic = {}
    user = request.user
    print("user role is: ", user_role)
    first_name = fullnames[0]
    last_name = ''
    if (len(fullnames) > 1):
        last_name = fullnames[1]
    print("1st names are: ", first_name)
    print("2nd names are: ", last_name)
    # User.objects.get(username=user_name, password=password)
    print("\n\tlogin data: ", user)

    email_exists = User.objects.filter(email=email).exists()
    username_exists = User.objects.filter(username=user_name).exists()

    # email_exists = (len(User.objects.filter(email=email)).exists)
    # username_exists = (len(User.objects.filter(username=user_name).exists))
    print(f"username {user_name} status: {username_exists}")
    print(f"email {email} status: {email_exists}")

    valid_object = [
        {"type": "email", "valid": email_exists},
        {"type": "username", "valid": username_exists},
        {"type": "password", "valid": True}

    ]

    if user.is_anonymous is True:
        try:
            if ((email_exists) or (username_exists)):
                response_dic = {'status_code': 404, 'data': valid_object,
                                'message': 'user error, email already exists'}
                return Response(response_dic)
            permission = Permission.objects.get(codename='can_view_dashboard')
            print("\n\t\tgotten permission: ", permission)

            # user_form = NewUserForm(
            #    request.POST or None, request.FILES or None, initial={'first_name':first_name, 'last_name':last_name, 'email':email,'username':user_name}
            #    )
            # if user_form.is_valid():
            #    print("\n form is valid")
            # else:
            #    print("\nform is invalid")
            # user_x = send_verification_email(request, user_form)
            # print("\n\n\tinactive user is: ", user_x)
            # if user_x is not None:
            #    user_x.first_name = first_name
            #    user_x.last_name = last_name
            #    user_x.set_password(password)
            #    user_x.save()
            user_x = User.objects.create_user(
                username=user_name, email=email, password=password, first_name=first_name, last_name=last_name)
            print("\n\n\tcreated new active user is: ", user_x)

            # user_x.save()
            user_x.user_permissions.add(permission)
            apicredentials = makeAPICredentials(user_x)
            print("\n\tcreated user: ", apicredentials)
            if (apicredentials is not None):
                dashboard_role = dashboard_constants[user_role]
                print("using dashboard role: ", dashboard_role)
                dashboard_user = DashboardUsers(
                    user=user_x, user_role=dashboard_role, internal_token=apicredentials)
                dashboard_user.save()
                # EdocVerify().send_email_verification(request, dashboard_user)

                login(request, user_x)
                name_dic = {'status_code': 200, 'name': user_x.get_username()}
                return Response(name_dic)
            else:
                name_dic = {'status_code': 500, 'message': 'server error'}
                return Response(name_dic)
        except:
            traceback.print_exc()
            name_dic = {'status_code': 500,
                        'message': 'user error, email or username exists'}
            return Response(name_dic)
    else:
        print("\n\tcreated user: ")
        name_dic = {'name': user.get_username()}
        return Response(name_dic)

# @api_view(['GET','POST'])
# Checks request method, returns loginGet for GET, error for others


@csrf_exempt
# @login_required(login_url="/dashboard/login")
@permission_required('airtimeapi.can_view_dashboard', login_url="/dashboard/login")
def dashboard(request):
    request_user = request.user
    if request_user.is_authenticated:
        print(f"user {request_user} is authenticated")
    request_method = request.method
    if request_method == "GET":
        print("using get ")
        return loginGet(request)
    else:
        return JsonResponse({"message": "method not accepted"})


@csrf_exempt
def getPublic(request):
    request_user = request.user
    request_method = request.method
    if request_method == "GET":
        print("using get ")
        url_name = request.path
        file_name = (url_name.split('/')[-1])+".html"
        print("Using url: ", file_name)
        return render(request, file_name)


@csrf_exempt
def xdashboard(request):
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
    request_method = request.method
    print("request method : ", request_method)
    if request_method == "GET":
        print("using get ")
        return loginGet(request)
        # return render(request, "page-register.html")
    requester = request.body
    print("request form is: ", requester)
    # user_name = requester['username']
    # password = requester['password']

    user_name = request.POST.get('username', '')
    password = request.POST.get('password', '')
    name_dic = {}
    # uers_up = User.objects.exists(username=user_name,password=password)
    print("username: ", user_name)
    print('password : ', password)
    is_authen = request.user
    print("is authenticated: ", is_authen.username)
    try:
        # user = authenticate(request,username=user_name, password=password)
        user = User.objects.get(username=user_name, password=password)

        print("user: ", user)
        if user is not None:
            print("user is not none")
            # request, user
            print("login successfully: ")
            # request.session['user'] = user
            # return render(request,"index.html")
            name_dic = {'status_code': 200,
                        'message': 'user success', 'name': user.get_username()}
            return JsonResponse(name_dic)
        else:

            print("user status: ", user)
            return render(request, "page-login.html")
        # user = User.objects.get(username=user_name, password=password)

       # token,created=Token.objects.get_or_create(user=user)
        # print("\n\tcreated user: ",created)
        # name_dic = {'status_code':200,'message':'user success','name':user.get_username(),'token':token.key}
        # return Response(name_dic)
        return render(request, "index.html")
    except Exception:
        print("user error")
        traceback.print_exc()
        return render(request, "page-login.html")
        # return Response({"status_code":500,"message":"User error"})


def loginView(request):
    return render(request, "page-login.html")


def loginGet(request):
    user = request.user
    print("using user: ", user)
    verify_email_txt = '''<div class="alert alert-info" role="alert">
                        User not yet verified, <a href="/verification/user/verify-email/request-new-link/" class="alert-link">click here</a> to resend verification message.
                        </div>'''
    try:
        if (user.is_authenticated == True) and (user != None):
            # return redirect(servePage)
            request_user = request.user
            dashboard_user = DashboardUsers.objects.get(user=request_user)
            user_role = dashboard_user.user_role
            print("user role: ", user_role)
            print("request user: ", request_user)
            print("user already authenticated")

            verification_state = dashboard_user.is_active
            print("verification state: ", verification_state)
            template_ctx = {}
            if verification_state == False:
                template_ctx = {
                    "active_username": user.get_username(),
                    "verify_email_div": True,
                }
            else:
                template_ctx["active_username"] = user.get_username()

            requestContext = template_ctx
            # RequestContext(request)
            url_name = request.path
            file_name = url_name.split('/')[-1]
            print("Using url: ", file_name)
            if file_name == '':
                if (user_role == "super_admin"):
                    # requestContext.push(template_ctx)
                    template_ctx = requestContext
                    return render(request, "super_index.html", requestContext)
                elif (user_role == "admin"):
                    # requestContext.push(template_ctx)
                    template_ctx = requestContext
                    return render(request, "admin_index.html", requestContext)
                elif (user_role == "company"):
                    # requestContext.push(template_ctx)
                    template_ctx = requestContext
                    return render(request, "company_index.html", requestContext)
                else:
                    # requestContext.push(template_ctx)
                    template_ctx = requestContext
                    return render(request, "index.html", requestContext)
            else:
                # requestContext.push(template_ctx)
                template_ctx = requestContext
                return render(request, file_name, requestContext)
        else:
            # return redirect(servePage)
            return render(request, "page-login.html")
    except:
        traceback.print_exc()
        return render(request, "page-login.html")


@csrf_exempt
@permission_required('airtimeapi.can_view_dashboard', login_url="/dashboard/login")
def generateAPICredentials(request):
    get_params = request.body
    print("request params are: ", get_params)
    username = random.randint(0, sys.maxsize)
    passwd = uuid.uuid4().hex
    api_permission = Permission.objects.get(codename='can_view_api')
    user_x = User.objects.create_user(username=username, password=passwd)
    # user_x.is_active = True
    # user_x.save()

    user_x.user_permissions.add(api_permission)
    token = Token.objects.create(user=user_x)
    # passwd = str(token.key)
    btn_type = request.POST.get("type")

    print("\n\t received btn: ", btn_type)
    is_pdt_key = True if btn_type == "pdt_key" else False
    print("\n\t is pdt key: ", is_pdt_key)
    apicredentials = APIcredentials(
        owner=request.user, token_user=user_x, token=token, is_production_key=is_pdt_key)
    apicredentials.save()
    print("username is: ", username)
    print("password is: ", passwd)
    return JsonResponse({"status_code": 200, "data": {"api_username": str(username), "api_password": passwd}})


def redirectUser(request):
    print("redirecting user")
    return redirect("/dashboard/")


def makeAPICredentials(for_user):
    username = random.randint(0, sys.maxsize)
    passwd = uuid.uuid4().hex
    user_x = User.objects.create_user(username=username, password=passwd)
    # user_x.is_active = True
    # user_x.save()
    api_permission = Permission.objects.get(codename='can_view_api')
    user_x.user_permissions.add(api_permission)

    token = Token.objects.create(user=user_x)

    apicredentials = APIcredentials(
        owner=for_user, token_user=user_x, token=token, is_internal_key=True)
    apicredentials.save()
    return apicredentials


@api_view(["POST"])
def loginUser(request):
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
    logging.info("request form is: "+str(requester))
    user_name = requester['username']
    password = requester['password']
    is_authen = request.user
    print("is authenticated: ", is_authen)

    try:
        user = User.objects.get(username=user_name)
        user_active_state = user.is_active
        if user_active_state == False:
            return JsonResponse({"status_code": 401, "data": {"message": "User is not yet verified"}})
        user = authenticate(request, username=user_name, password=password)

        print("\n\tauthenticated user: ", user)
        if user is not None:
            print("user is not none")
            user_perms = user.get_all_permissions()
            print("\n\tuser permissions: ", user_perms)
            login(request, user)
            print("login successfully: ")
            # request.session['user'] = user
            # return render(request,"index.html")
            name_dic = {'status_code': 200,
                        'message': 'user success', 'name': user.get_username()}
            return JsonResponse(name_dic)
        else:

            print("user status: ", user)
            name_dic = {'status_code': 500, "data": {
                'message': 'Invalid Credentials'}}
            return JsonResponse(name_dic)
            # return  render(request,"page-login.html")
    except Exception:
        print("user error")
        traceback.print_exc()
        name_dic = {'status_code': 500, "data": {
            'message': 'Invalid Credentials'}}
        return JsonResponse(name_dic)
        # return render(request,"page-login.html")


def logoutUser(request):
    # request.session.flush()
    # request.user.auth_token.delete()
    logout(request)
    return redirect("/dashboard")
    # return render(request,"page-login.html")

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])


@permission_required('airtimeapi.can_view_dashboard', login_url="/dashboard/login")
def getLogs(request):
    """## _summary_

    ### Args:
        - `request (_type_)`: _description_

    ### Returns:
        - `_type_`: _description_
    """
    request_user = request.user
    print("\n\n\trequested by: ", request_user.username)
    get_body = request.GET  # .urlencode()
    print("\n\tGet request body: ", get_body)
    # json_request = json.loads(request.body)
    # log_type = json_request["category"]
    draw_id = item_no = request.GET.get('draw')
    log_type = request.GET.get('type')
    item_index = request.GET.get('start')
    item_no = request.GET.get('length')
    print(f"data table is: {log_type} {item_index} and total: {item_no} with draw id: {draw_id}")

    # log_columns,
    log_data = Logs().getLog(request_user, log_type, get_body)
    print(f"\n\n\t\ttotal rows: {len(log_data)}\n\n")

    more_records = log_data
    # [int(item_index): (int(item_index)+1)+int(item_no)]
    print("xlog data: ", more_records)
    # "columns":log_columns,
    log_response = {
        "draw": draw_id,
        "recordsTotal": len(log_data),
        "recordsFiltered": len(log_data),
        "data": more_records
    }
    return JsonResponse(log_response)


@csrf_exempt
@permission_required('airtimeapi.can_view_dashboard', login_url="/dashboard/login")
def addAdmin(request):
    user = request.user
    fullnames = str(request.POST.get('fullnames')).split(' ')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    telno = request.POST.get('telno')
    first_name = fullnames[0]
    last_name = ''
    if (len(fullnames) > 1):
        last_name = fullnames[1]

    print(f"creating admn {username} {password} {email} {telno}")

    email_exists = (len(User.objects.filter(email=email)) == 0)
    username_exists = (len(User.objects.filter(username=username)) == 0)
    # telno_exists =
    print(f"username {username} status: {username_exists}")
    print(f"email {email} status: {email_exists}")

    valid_object = [
        {"type": "email", "valid": email_exists},
        {"type": "username", "valid": username_exists},
        {"type": "password", "valid": True}

    ]

    if user.is_anonymous is not True:
        try:
            if ((email_exists == False) or (username_exists == False)):
                response_dic = {'status_code': 404, 'data': valid_object,
                                'message': 'user error, email already exists'}
                return JsonResponse(response_dic)

            user_x = User(username=username, email=email, password=password,
                          first_name=first_name, last_name=last_name)
            user_x.save()
            apicredentials = makeAPICredentials(user_x)
            print("\n\tcreated user: ", apicredentials.owner.username)
            if (apicredentials is not None):
                dashboard_role = "admin"
                print("using dashboard role: ", dashboard_role)
                dashboard_user = DashboardUsers(
                    user=user_x, user_role=dashboard_role, created_by=user, internal_token=apicredentials)
                dashboard_user.save()
                name_dic = {'status_code': 200, 'name': user_x.get_username()}
                return JsonResponse(name_dic)
            else:
                name_dic = {'status_code': 500, 'message': 'server error'}
                return JsonResponse(name_dic)
        except:
            traceback.print_exc()
            name_dic = {'status_code': 500,
                        'message': 'user error, email or username exists'}
            return JsonResponse(name_dic)
    else:
        print("\n\tcreated user: ")
        name_dic = {'status_code': 500, 'message': 'user auth error'}
        return JsonResponse(name_dic)

    # return JsonResponse({valid_object})


@csrf_exempt
@permission_required('airtimeapi.can_view_dashboard', login_url="/dashboard/login")
def requestVerifyDocs(request):

    current_user = request.user

    if current_user == None:
        return JsonResponse({'success': False, 'error':  'Auth Error'})
    request_files = request.FILES
    request_files_len = len(request.FILES)
    print("\n\t files uploaded: ", request_files)
    print("\n\t files uploaded: ", len(request.FILES))
    files = []

    for requested_index in range(0, request_files_len):
        files.append(request_files.get(f"document-{requested_index}"))

    no_of_files = len(files)
    print(f"\n\tnumber of files uploaded is: {no_of_files}")
    if request.method == 'POST' and no_of_files > 0:
        # document = request.FILES['document']
        print("uploaded doc: ", files)
        print("current user: ", current_user.username)
        time_stamp = int(time.time())

        user_name = current_user.username
        tmp_name = f"{user_name}_{time_stamp}"
        tmp_zip = f"{tmp_name}.zip"
        zip_file_path = os.path.join(settings.MEDIA_ROOT, "uploads", tmp_zip)

        co_name = request.POST.get('name')
        co_email = request.POST.get('email')
        co_telno = request.POST.get('telno')
        # print(f"request form is: {co_name} {co_email} {co_telno}")
        # company = Companies.objects.create(user=current_user,
        #                    company_name = co_name,
        #                    company_telno = co_telno,
        #                    company_email = co_email)
        zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
        # for afile in files:
        #    print("\n\t afile: ", afile)
        #    company_doc = Uploaded_File(uploaded_file= afile)
        #    company_doc.save()
        #    uploaded_file_names = company_doc.uploaded_file.name.split('/')
        #    uploaded_file_name = uploaded_file_names[1]
        # os.path.join(settings.MEDIA_ROOT,str(company_doc.uploaded_file))
        #    print("uploaded file name: ", uploaded_file_name)
        #    zippath = os.path.join(settings.MEDIA_ROOT,uploaded_file_names[0],uploaded_file_name)

        #    print("saving file zip at: ", zippath)
        #    zip_file.write(zippath,arcname=uploaded_file_name)

        #    company_doc.delete()
        #    os.remove(zippath)
        # company_doc.save()
        # zip_file.close()
        # zip_alt = f"uploads/{tmp_zip}"
        # zip_file_name = zip_file.filename
        # print("\n\tcreated zip file: ", zip_file_name)
        company = Companies.objects.create(user=current_user,
                                           company_name=co_name,
                                           company_telno=co_telno,
                                           # ,company_doc = zip_alt)
                                           company_email=co_email)

        for afile in files:
            company_doc = Uploaded_File(uploaded_file=afile)
            company_doc.save()
            company.company_docs.add(company_doc)
            company.save()

        print("\n\tmade zip file: ", zipfile)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No file uploaded'})


@csrf_exempt
@permission_required('airtimeapi.can_view_dashboard', login_url="/dashboard/login")
def verifyDoc(request):
    current_user = request.user

    if request.method == "POST":
        if current_user == None:
            return JsonResponse(
                {
                    "status": 400,
                    "message": "user auth error"
                }
            )
        doc_uuid = request.POST.get("co_uuid")
        print("verifying docs: ", doc_uuid)

        current_company = Companies.objects.get(company_uuid=doc_uuid)
        current_company.verification_status = True
        current_company.save()
        return JsonResponse({
            "status": 200,
            "message": {
                "verified": f"verified: {current_company.company_name}"
            }
        })


@csrf_exempt
@require_POST
@permission_required('airtimeapi.can_view_dashboard', login_url="/dashboard/login")
def getVerificationDocs(request):
    company_post = request.POST
    print("company post: ", company_post)
    company_uuid = request.POST.get("co_uuid")
    company_doc_index = request.POST.get("doc_index")
    if not company_doc_index:
        company_doc_index = 0

    co_docs = Logs().getCompanyDocs(company_uuid)
    # company = Companies.objects.get(company_uuid=company_uuid)
    # co_docs = company.company_docs
    # print("company docs: ",co_docs)
    # print("company docs len: ", len(co_docs))
    # co_doc = co_docs#[0].uploaded_file
    print("\n\n\tcompany doc: ", co_docs)
    # if co_doc:
    #    co_doc_name = co_doc.name
    #    print("getting document: ",co_doc.name)
    #    response = HttpResponse(co_doc.read(), headers={
    #        "content_type":'application/pdf',
    #        "Content-Disposition": f'attachment; filename="{co_doc_name}"'
    #        })
    # response['Content-Disposition'] = 'attachment; filename="%s"' % co_doc.name
    response_data = JsonResponse({
        "status": 200,
        "message": co_docs
    })
    return response_data


@csrf_exempt
@require_POST
@permission_required('airtimeapi.can_view_dashboard', login_url="/dashboard/login")
def getVerificationDoc(request):
    company_post = request.POST
    print("company post: ", company_post)
    company_uuid = request.POST.get("co_uuid")
    company_doc_index = int(request.POST.get("doc_index"))
    if not company_doc_index:
        company_doc_index = 0
    elif company_doc_index > 4:
        company_doc_index = 0
    elif company_doc_index < 0:
        company_doc_index = 0
    company = Companies.objects.get(company_uuid=company_uuid)
    co_docs = company.company_docs.all()[company_doc_index].uploaded_file
    print("company docs: ", co_docs)
    print("company docs len: ", len(co_docs))
    co_doc = co_docs  # [0].uploaded_file
    print("\n\tcompany doc: ", co_doc)
    if co_doc:
        co_doc_name = co_doc.name
        print("getting document: ", co_doc.name)
        response = HttpResponse(co_doc.read(), headers={
            "content_type": 'application/pdf',
            "Content-Disposition": f'attachment; filename="{co_doc_name}"'
        })
        # response['Content-Disposition'] = 'attachment; filename="%s"' % co_doc.name
        return response
    else:
        return HttpResponseNotFound('File not found')


@csrf_exempt
@permission_required('airtimeapi.can_view_dashboard', login_url="/dashboard/login")
def verifyKey(request):
    key_post = request.POST
    print("company post: ", key_post)

    try:
        key_uuid = request.POST.get("key_uuid")
        print("using key uuid: ", key_uuid)
        key = APIcredentials.objects.get(token_uuid=key_uuid)
        key.is_validated = True
        key.save()
        return JsonResponse({
            "status": 200,
            "message": "Token Verified"
        })
    except:
        traceback.print_exc()
        return JsonResponse({
            "status": 400,
            "message": "server error"
        })


@csrf_exempt
def disableKey(request):
    pass
