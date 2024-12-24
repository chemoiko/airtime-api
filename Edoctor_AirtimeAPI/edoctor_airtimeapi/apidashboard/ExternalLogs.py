import requests
from django.urls import resolve,reverse, reverse_lazy
def getExternalLog(token,log_type,log_params):
    
    external_url = "http://127.0.0.1:8000"
    external_endpoint = reverse_lazy("airtimeapi:getLogs")#, current_app="airtimeapi").url_name
    print("using external endpoint: ",external_endpoint)
    headers = {'Authorization': f"Token {token}"}
    log_url = f"{external_url}{external_endpoint}?{log_params}"

    print(f"external url: {log_url} with extra headers {headers}")
    response = requests.get(log_url, headers=headers)
    response_body = response.json()
    print("extra logs response: ",response_body)
    #assert response.status_code == 200
    #assert response_body["authenticated"] == True
    #assert response_body["user"] == "user"
    return response_body['data']
