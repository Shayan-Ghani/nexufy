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
            if not isinstance(repo_names, list):
                raise TypeError("repository names must be list!")
            self.repo_names = repo_names               
        else:
            raise ValueError("repository names can't be empty!")
        
        if base_url != None:
            if not isinstance(base_url, str):
                raise TypeError("base_url must be string!")
            self.base_url = base_url               
        else:
            raise ValueError("base_url can't be empty!")        
        
        if file_path != None:
            if not isinstance(file_path, str):
                raise TypeError("file_path must be string!")
            self.file_path = file_path               
        else:
            self.file_path = f"{path.dirname(__file__)}/data.txt"

        if username != None:
            if not isinstance(username, str):
                raise TypeError("username must be string!")
            self.username = username               
        else:
            raise ValueError("username can't be empty!")

        if password != None:
            if not isinstance(password, str):   
                raise TypeError("password must be string!")
            self.password = password               
        else:
            raise ValueError("password can't be empty!")

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
            response = requests.get(endpoint, auth=self.auth_info)
            self.responses.append(response)
        return self.responses

    def write_to_file(self, data=None, file_path=None):
        if data != None:
            if not isinstance(data, str):
                raise TypeError("data must be str!")

        if file_path != None:
            if not isinstance(file_path, str):
                raise TypeError("file_path must be string!")
            self.file_path = file_path

        with open(self.file_path, 'w') as f:
            f.write(data)


    def get_items(self, responses=None):
        if responses != None:
            if not isinstance(responses, list):
                raise TypeError("repository names must be list!")
            self.responses = responses
        
        json = responses[0].json()
        data = []
        data = json.get('items', [])
        
        if len(self.responses) > 1:
            data.clear()
            for response in self.responses:
                json = response.json()
                item = json.get('items', [])
                data.append(item)

        #TODO : make package variables use self to have access when an object created!
        for package in data:
            npm_info = package.get('npm', {})
            package_name = npm_info.get('name')
            package_version = npm_info.get('version')

            package_size_bytes = package.get('fileSize')
            package_size_kb = package_size_bytes / (1024)
            package_last_downloaded = package.get('lastDownloaded')

        return package_name, package_version, package_size_kb, package_last_downloaded
    
    def get_len(self):
        p_len = len(self.repo_names)
        return p_len