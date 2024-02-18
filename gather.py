from requests import get
from os import path

class NexusRepo():
    repo_names = []
    base_url = ""
    _repo_path = base_url + "service/rest/v1/search/assets"
    file_path = f"{path.dirname(__file__)}/data.txt"
    username = ""
    password = ""
    auth_info = ()

    def __init__(self, repo_names:list = [] , base_url:str = "", username:str = "", password:str = ""):

        assert isinstance(repo_names, list) 
        self.repo_names = repo_names
                 
        assert isinstance(base_url, str)
        self.base_url = base_url              
        
        assert isinstance(username, str)
        self.username = username               
        
        assert isinstance(password, str)
        self.password = password

    def _set_file_path(self, file_path:str = "") -> str:
        if file_path != "":
            assert isinstance(file_path, str)
            if not path.exists(file_path):
                raise Exception(f"path {file_path} doesn't exist!")
            self.file_path = file_path
        
        return self.file_path
    
    def write_to_file(self, data:str = "", path:str = ""):
        
        file_path = self._set_file_path(file_path=path)

        with open(file_path, 'w') as f:
            f.write(data)
   

    def auth(self, username:str = "", password:str = "", base_url:str = ""):
        if username != "" and password != "":
            assert isinstance(username, str)
            self.username = username
            assert isinstance(password, str)
            self.password = password
        
        if base_url != "":
            assert isinstance(base_url, str)
            self.base_url = base_url

        self._repo_path = self.base_url + "service/rest/v1/search/assets"

        self.auth_info = (self.username, self.password)
    
    def get_items(self) -> list:
        data = []
        for name in self.repo_names:
            endpoint = self._repo_path + f'?repository={name}'
            response = get(endpoint, auth=self.auth_info)
            # data = [r.json().get('items', []) for r in response]
            data.append(response.json().get('items', []))
            
        return data

    def path(self) -> list:
        path = []
        for response in self.get_items():
            path += [r.get('path') for r in response]
            
        # return data
        return path
    
    def npm_name(self) -> list:
        names = []
        for response in self.get_items():
            names += [r.get('npm', {}).get('name') for r in response]
        return names
    
    def npm_version(self) -> list:
        versions = []
        for response in self.get_items():
            versions += [r.get('npm', {}).get('version') for r in response]
        return versions
    
    def size(self) -> list:
        f_size = []
        for response in self.get_items():
            f_size = [r.get('fileSize') / (1024) for r in response]

        return f_size

    def last_downloaded(self) -> list:
        d_time = []
        for response in self.get_items():
            d_time += [r.get('lastDownloaded') for r in response]
            
        return d_time

        #TODO : make package variables use self to have access when an object created!
        #TODO : break every package into isolated methods
        #TODO : typing and validation. default and search for efficiency, (pydantic).
        #TODO : create seperate methods for seperate data from nexus.
        #TODO : add name as the defult value for all methods.
    
    def get_len(self , items: list = []) -> int:
        return len(items)
