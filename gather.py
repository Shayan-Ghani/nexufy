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
    
    def _get_response(self) -> list:
        data = []
        for name in self.repo_names:
            endpoint = self._repo_path + f'?repository={name}'
            response = get(endpoint, auth=self.auth_info)
            # data = [r.json().get('items', []) for r in response]
            data.append(response.json().get('items', []))
            
        return data

    def get_items(self) -> list:
        info = []
        for response in self._get_response():
            info += [r.get('path') for r in response]
            
        # return data
        return info
    
        #TODO : make package variables use self to have access when an object created!
        #TODO : break every package into isolated methods
        #TODO : typing and validation. default and search for efficiency, (pydantic).

    #     for package in data:
    #         npm_info = package.get('npm', {})
    #         package_name = npm_info.get('name')
    #         package_version = npm_info.get('version')

    #         package_size_bytes = package.get('fileSize')
    #         package_size_kb = package_size_bytes / (1024)
    #         package_last_downloaded = package.get('lastDownloaded')

    #     return package_name, package_version, package_size_kb, package_last_downloaded
    
    def get_len(self , items: list = []) -> int:
        return len(items)
