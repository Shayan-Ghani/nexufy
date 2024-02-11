import requests
from os import path

class GetNexusRepo():
    repo_names = []
    base_url = ""
    repo_path = base_url + "service/rest/v1/search/assets"
    file_path = f"{path.dirname(__file__)}/data.txt"
    username = ""
    password = ""
    auth_info = ()
    responses = []

    def __init__(self, repo_names=None , base_url=None, file_path=None, username=None, password=None):
        if repo_names != None:
            if not type(repo_names) is list:
                raise("repository names must be list!")
            self.repo_names = repo_names               
        else:
            raise("repository names can't be empty!")
        
        if base_url != None:
            if not type(base_url) is str:
                raise("base_url must be string!")
            self.base_url = base_url               
        else:
            raise("base_url can't be empty!")        
        
        if file_path != None:
            if not type(file_path) is str:
                raise("file_path must be string!")
            self.file_path = file_path               
        else:
            self.file_path = f"{path.dirname(__file__)}/data.txt"

        if username != None:
            if not type(username) is str:
                raise("username must be string!")
            self.username = username               
        else:
            raise("username can't be empty!")


        if password != None:
            if not type(password) is str:
                raise("password must be string!")
            self.password = password               
        else:
            raise("password can't be empty!")

    def auth(self, username=None, password=None, base_url=None):
        if username != None and password != None and base_url != None:
            self.username = username
            self.password = password
            self.base_url = base_url 
            self.auth_info = (username, password)

        self.auth_info = (self.username, self.password)
        

        self.repo_path = self.base_url + "service/rest/v1/search/assets"

        for name in self.repo_names:
            endpoint = self.repo_path + f'?repository={name}'
            self.responses.append(requests.get(endpoint, auth=self.auth_info))
            return self.responses


