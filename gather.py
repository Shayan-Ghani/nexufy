import requests
from os import path

class NexusRepo():

    def __init__(self, repo_names=None , base_url=None, file_path=None, username=None, password=None):

        self.repo_names = []
        self.base_url = ""
        self._repo_path = base_url + "service/rest/v1/search/assets"
        self.file_path = f"{path.dirname(__file__)}/data.txt"
        self.username = ""
        self.password = ""
        self.auth_info = ()
        self.responses = []

        if repo_names != None:
            assert isinstance(repo_names, list)
            self.repo_names = repo_names               
        else:
            raise ValueError("repository names can't be empty!")
        
        if base_url != None:
            assert isinstance(base_url, str)
            self.base_url = base_url              
        else:
            raise ValueError("base_url can't be empty!")        
        
        if file_path != None:
            assert isinstance(file_path, str)
            self.file_path = file_path               
        else:
            self.file_path = f"{path.dirname(__file__)}/data.txt"

        if username != None:
            assert isinstance(username, str)
            self.username = username               
        else:
            raise ValueError("username can't be empty!")

        if password != None:
            assert isinstance(password, str)
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
        
        self._repo_path = self.base_url + "service/rest/v1/search/assets"

        for name in self.repo_names:
            endpoint = self._repo_path + f'?repository={name}'
            response = requests.get(endpoint, auth=self.auth_info)
            self.responses.append(response)
        return self.responses

    def write_to_file(self, data=None, file_path=None):
        if data != None:
            assert isinstance(data, str)
        if file_path != None:
            assert isinstance(file_path, str)
            self.file_path = file_path

        with open(self.file_path, 'w') as f:
            f.write(data)


    def get_items(self, responses=None):
        if responses != None:
            assert isinstance(responses, list)
            self.responses = responses
        
        data = [r.json().get('items', []) for r in self.responses]
        
        return data
        #TODO : make package variables use self to have access when an object created!
        #TODO : break every package into isolated methods
        #TODO : typing and validation. default and search for efficiency, (pydantic).
        #TODO : Change equall sign to is not for None checking.
        #TODO : use pythonic for better python-native code.
        #TODO : remove single-check for get_items
        #TODO : try to call methods within the class to get the getter data don't handle them again. 
        #TODO you don't have to get the arguments for different parameters in every methods that's why we use class cause we already have its state.
        
    #     for package in data:
    #         npm_info = package.get('npm', {})
    #         package_name = npm_info.get('name')
    #         package_version = npm_info.get('version')

    #         package_size_bytes = package.get('fileSize')
    #         package_size_kb = package_size_bytes / (1024)
    #         package_last_downloaded = package.get('lastDownloaded')

    #     return package_name, package_version, package_size_kb, package_last_downloaded
    
    # def get_len(self):
    #     p_len = len(self.repo_names)
    #     return p_len
