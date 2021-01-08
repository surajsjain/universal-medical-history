import requests
from django.conf import settings

def upload(file_to_upload, id=settings.SLATE_ID, auth_code=settings.SLATE_AUTH_CODE):
        url = 'https://uploads.slate.host/api/public/' + id
        auth_request = 'Basic ' + str(auth_code)
        headers = {'Authorization': auth_request}
        files = {'media': file_to_upload}
        # print("HERE")
        response = requests.post(url=url,headers = headers,files = files)
        return response.json()["url"]

def get_slate_by_id(id=settings.SLATE_ID, auth_code=settings.SLATE_AUTH_CODE):
    url = 'https://slate.host/api/v1/get-slate'

    auth_request = 'Basic ' + str(auth_code)
    headers = {'Authorization': auth_request}

    data = {'id' : id}

    response = requests.get(url=url, data = data, headers = headers)
    return response.json()

def get_all(auth_code=settings.SLATE_AUTH_CODE):
    url = 'https://slate.host/api/v1/get'

    auth_request = 'Basic ' + str(auth_code)
    headers = {'Authorization': auth_request}

    data = {'private' : 'false'}

    response = requests.get(url=url, data = data, headers = headers)

    return response.json()