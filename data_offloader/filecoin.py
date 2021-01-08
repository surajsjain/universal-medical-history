import requests

def upload(file_to_upload, id =""):
        url = 'https://uploads.slate.host/api/public/' + id
        headers = {'Authorization': 'Basic SLA75c4d6f0-c956-4e01-98d7-c52d72f3b948TE'}
        files = {'media': open(file_to_upload, 'rb')}
        # print("HERE")
        response = requests.post(url=url,headers = headers,files = files)
        return response.json()["url"]

def get_slate_by_id(id):
    url = 'https://slate.host/api/v1/get-slate'

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic SLA75c4d6f0-c956-4e01-98d7-c52d72f3b948TE'}
    # data = {'id' : 'bbc27639-8110-4fb9-97e4-6d0f5d43e05e'}
    data = {'id' : id}

    response = requests.get(url=url, data = data, headers = headers)
    return response.json()

def get_all():
    url = 'https://slate.host/api/v1/get'

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic SLA75c4d6f0-c956-4e01-98d7-c52d72f3b948TE'}
    # data = {'id' : 'bbc27639-8110-4fb9-97e4-6d0f5d43e05e'}
    data = {'private' : 'false'}

    response = requests.get(url=url, data = data, headers = headers)

    return response.json()