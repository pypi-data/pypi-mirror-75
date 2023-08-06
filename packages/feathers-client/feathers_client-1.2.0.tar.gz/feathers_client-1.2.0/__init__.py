import json
import requests
from collections import namedtuple

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


class FeathersService:
    
    def __init__(self,host,email=None,password=None):
        self.host=host
        self.email=email
        self.password=password
        self.feathers=Feathers(host,email,password)
        self.is_authenticated=False

    def service(self,name):
        self.service=name
        return {find:self.find}

    def authenticate(self):
        self.feathers._auto_login()
        self.is_authenticated=True
        return self
    
    def find(self,params={},data={}):
        return self.feathers._find(self.service,params,data) if self.is_authenticated else None

    def get(self,id,params={},data={}):
        return self.feathers._get(self.service,id,params,data) if self.is_authenticated else None

    def create(self,params={},data={}):
        return self.feathers._create(self.service,params,data) if self.is_authenticated else None

    def update(self,id,params={},data={}):
        return self.feathers._update(self.service,id,params,data) if self.is_authenticated else None

    def patch(self,id,params={},data={}):
        return self.feathers._patch(self.service,id,params,data) if self.is_authenticated else None

    def delete(self,params={},data={}):
        return self.feathers._delete(self.service,id,params,data) if self.is_authenticated else None

    
class Feathers:
    
    def __init__(self,host,email=None,password=None):
        self.host=host
        self.email=email
        self.password=password
        
    def _auto_login(self):
        response = self._login(self.email,self.password)
        print(response.status_code)
        if response.status_code in [200,201]:
            self.user=json2obj(response.text)
        else:
            raise Exception(response.text)

    def _login(self,email=None,password=None):
        url="{}/authentication".format(self.host)

        payload = {
            "strategy":"local",
            "email":self.email if email is None else email,
            "password":self.password if password is None else password,
        }
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        return response

    def _find(self,service,params={},data={},auth_token=None):
        url="{}/{}".format(self.host,service)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.user.accessToken if auth_token is None else auth_token)
        }

        response = requests.request("GET", url, headers=headers,params=params,data = json.dumps(data))
        print(response.status_code)
        if response.status_code in [200,201]:
            return response.json()
        else:
            raise Exception(response.text)
    def _get(self,service,id,params={},data={},auth_token=None):
        url="{}/{}/id".format(self.host,service,id)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.user.accessToken if auth_token is None else auth_token)
        }

        response = requests.request("GET", url, headers=headers,params=params,data = json.dumps(data))
        print(response.status_code)
        if response.status_code in [200,201]:
            return response.json()
        else:
            raise Exception(response.text)
    def _create(self,service,params={},data={},auth_token=None):
        url="{}/{}".format(self.host,service)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.user.accessToken if auth_token is None else auth_token)
        }

        response = requests.request("POST", url, headers=headers,params=params,data = json.dumps(data))
        print(response.status_code)
        if response.status_code in [200,201]:
            return response.json()
        else:
            raise Exception(response.text)
    def _update(self,service,id,params={},data={},auth_token=None):
        url="{}/{}/{}".format(self.host,service,id)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.user.accessToken if auth_token is None else auth_token)
        }

        response = requests.request("PUSH", url, headers=headers,params=params,data = json.dumps(data))
        print(response.status_code)
        if response.status_code in [200,201]:
            return response.json()
        else:
            raise Exception(response.text)
    def _patch(self,service,id,params={},data={},auth_token=None):
        url="{}/{}/{}".format(self.host,service,id)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.user.accessToken if auth_token is None else auth_token)
        }

        response = requests.request("PATCH", url, headers=headers,params=params,data = json.dumps(data))
        print(response.status_code)
        if response.status_code in [200,201]:
            return response.json()
        else:
            raise Exception(response.text)

    def _delete(self,service,params={},data={},auth_token=None):
        url="{}/{}".format(self.host,service)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.user.accessToken if auth_token is None else auth_token)
        }

        response = requests.request("DELETE", url, headers=headers,params=params,data = json.dumps(data))
        print(response.status_code)
        if response.status_code in [200,201]:
            return response.json()
        else:
            raise Exception(response.text)