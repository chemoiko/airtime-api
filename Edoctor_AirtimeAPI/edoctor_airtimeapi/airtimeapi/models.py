# from django.db import models

# Create your models here.
# from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from datetime import date

from django.contrib.auth.models import User, AbstractUser
from rest_framework.authtoken.models import Token

from apidashboard.models import APIcredentials
# Create your models here.
import traceback


def getOwner(token_id):
    try:
        token = APIcredentials.objects.get(token_user=token_id)
        owner = token.owner
        return owner
    except:
        traceback.print_exc()
        return token_id


class Data(models.Model):
    # using = "default"
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

# class User(models.Model):
#    username = models.CharField(max_length=200)
#    email = models.EmailField()
#    password = models.CharField(max_length=200)

#    def __str__(self):
#        return self.username

# class Data(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    telno = models.CharField(max_length=200)
#    amount = models.IntegerField()

#    def __str__(self):
#        return self.telno

# class Token(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    key = models.CharField(max_length=200)

#    def __str__(self):
#        return self.key


class TokenUserModel(models.Model):

    class Meta:
        permissions = (
            ("can_view_dashboard", "can login and use the dashboard"),
            ("can_view_api", "can use token based login to use the airtime api")
        )


class APIUsers(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(null=False, max_length=255)
    is_super = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars")
    admin_request = models.BooleanField(default=False)


class Company(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=255)
    is_verified = models.BooleanField(default=False)
    document = models.FileField(upload_to="documents")
    owner = models.ForeignKey(
        User, related_name="company_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()


class AirtimeTransaction(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telno = models.CharField(max_length=200)
    amount = models.IntegerField()
    # airtime transaction method: SEND, RECV
    method = models.CharField(max_length=5)
    status = models.CharField(max_length=200)
    endpoint = models.CharField(max_length=200)
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="airtime_transaction_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.telno
# AirtimeTransaction


class MSISDNInfo(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    msisdn = models.CharField(max_length=200)
    # info = models.TextField()
    status = models.CharField(max_length=200)
    endpoint = models.CharField(max_length=200)
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="msisdn_info_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.msisdn


class AirtimePurchase(models.Model):
    # using = "default"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    netwrk = models.CharField(max_length=200)
    amount = models.IntegerField()
    endpoint = models.CharField(max_length=200)
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="airtime_purchase_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.netwrk


class MMFundsDeposit(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    telno = models.CharField(max_length=200)
    amount = models.IntegerField()
    endpoint = models.CharField(max_length=200)
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="mmfunds_deposit_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.telno


class MMFundsWithdraw(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    telno = models.CharField(max_length=200)
    amount = models.IntegerField()
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="mmfunds_withdraw_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.telno


class BankDeposit(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    accno = models.CharField(max_length=200)

    amount = models.IntegerField()
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="bank_deposit_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.request_user


class InternalTransfer(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    sender_acc = models.CharField(max_length=200)
    recv_acc = models.CharField(max_length=200)
    amount = models.IntegerField()
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="internal_transfer_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.request_user


class WithdrawMoneyToBank(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    accno = models.CharField(max_length=200)
    amount = models.IntegerField()
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="withdraw_to_bank_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.request_user


class TransactionStatus(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=200)
    transaction_type = models.CharField(max_length=200)
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="transaction_status_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.transaction_id


class BankWithdrawStatus(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=200)
    amount = models.IntegerField()
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="bank_withdraw_status_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return self.transaction_id


class Balance(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    balance = models.JSONField(default={})
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="balance_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):
        return str(self.balance)


class MiniStatement(models.Model):
    # using = "default"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    total_transactions = models.CharField(max_length=200)
    response = models.JSONField(default={})
    request = models.JSONField(default={})
    ip = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="mini_statement_token_owner", null=True, on_delete=models.CASCADE)

    def save(self):
        self.owner = getOwner(self.user)
        # owner = models.ForeignKey(User, default=)
        return super().save()

    def __str__(self):

        return str(self.ip)
