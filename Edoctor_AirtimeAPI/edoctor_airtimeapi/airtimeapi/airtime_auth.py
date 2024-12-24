from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

import traceback

from apidashboard.models import APIcredentials
class AirtimeAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Your custom authentication logic goes here
        # For example, you might check a token in the request headers
        request_url = request.path

        if request.path == "/auth/register":
            print("is registration")
        user_name = request.headers.get('username')
        pwd = request.headers.get('password')
        if not user_name:
            print("no username")
            raise AuthenticationFailed('No UserName')
            return None
        if not pwd:
            print("no password")
            raise AuthenticationFailed('No Password')
            return None
        # Example: token is in the format "Token <token>"
        try:
            print("\n\n\tauthenticating user: ",user_name)
            print("\n\n\tauthenticating password: ",pwd)
            user = authenticate(username=user_name, password=pwd)
            print("\n\tuser is: ", user)
            if not user:
                raise AuthenticationFailed('Invalid UserName and Password')
                return None
            if user.has_perm("airtimeapi.can_view_api"):
                print("user authentication: ", user)
                api_credentials = APIcredentials.objects.get(token_user = user)
                is_production = api_credentials.is_production_key
                validation_status = user_type = api_credentials.is_validated
                if (is_production == True) and (validation_status == False):
                    raise AuthenticationFailed('Production Credentials Not Validated')
                    return None
                else:
                    return (user, None)
            else:
                raise AuthenticationFailed('Invalid User')
                return None
        except ValueError:
            traceback.print_exc()
            raise AuthenticationFailed('Invalid User')