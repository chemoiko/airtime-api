from django.forms import ModelForm
from apidashboard.models import DashboardUsers
from django.contrib.auth.models import User
class NewUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email"]
    #username = forms.CharField(label='Username', max_length=100)
    #password = forms.CharField(label='Password', widget=forms.PasswordInput)
    #email = forms.EmailField(label="email", max_length=100)
    #first_name = forms.CharField(label="FirstName", max_length=100)
    #second_name = forms.CharField(label="SecondName", max_length=100)
    #role = forms.CharField(label="user_role", max_length=10)