from django.db import models
from django.contrib.auth.models import User, AbstractUser
from rest_framework.authtoken.models import Token
from datetime import date,time, datetime

# Create your models here.
import uuid
USER_TYPES = (
    ("admin","admin"),
    ("super_admin","super_admin"),
    ("company","company"),
    ("developer","developer")
)

class DashboardPermModel(models.Model):
    class meta:
        permissions = [
                        ("can_view_dashboard","can access the dashboard"),
                        ("can_view_api","can access and use the api")
        ]

#class AirtimeAPIPerm(models.Model):
#    name = models.CharField(default="", max_length=50)
#    class meta:
#        permissions = [
#                        ("can_use_api","can access and use the api")
#        ]

class Uploaded_File(models.Model):
    uploaded_file = models.FileField(upload_to="tmp/")
    def __str__(self):
        return self.uploaded_file.name
class APIcredentials(models.Model):
    owner = models.ForeignKey(User, related_name="credential_owner", on_delete=models.CASCADE)
    
    token_user = models.ForeignKey(User, default=None, unique=True, null=True, related_name="token_username", on_delete=models.CASCADE)
    #token_uuid =  models.UUIDField(max_length=24, default=uuid.uuid4)
    token_uuid = models.UUIDField( 
         unique = True, 
         default = uuid.uuid4, 
         editable = False) 
    #token_uuid = models.CharField(max_length=255, unique=True, default=uuid.uuid4().hex)
    is_production_key = models.BooleanField(default=False)
    is_internal_key = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)

class DashboardUsers(models.Model):
    user = models.ForeignKey(User, related_name="dashboard_user", unique=True, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, choices=USER_TYPES, default="developer")
    internal_token = models.ForeignKey(APIcredentials,null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="created_by", on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_login = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    #request_count = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
class SuperAdmin(models.Model):
     user = models.ForeignKey(User, related_name="superadmin_user", on_delete=models.CASCADE)
     slave_user = models.ForeignKey(DashboardUsers, related_name="slave_user", on_delete=models.CASCADE)

class Companies(models.Model):
    user = models.ForeignKey(User, related_name="company_owner", on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, default="")
    company_uuid = models.UUIDField( 
         unique = True, 
         default = uuid.uuid4, 
         editable = False) 
    company_email = models.CharField(max_length=255, default="")
    company_telno = models.CharField(max_length=255, default="")
    company_doc = models.FileField(upload_to="uploads/", null=True)
    company_docs = models.ManyToManyField(Uploaded_File, related_name="company_docs", null=True)
    
    verification_status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)


class XAPIKeys(models.Model):
    #using = "default"
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    is_production = models.BooleanField(default=False)
   
