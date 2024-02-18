from requests import get
from os import path

class NexusRepo():
    repo_names = []
    base_url = ""
    _repo_path = base_url + "service/rest/v1/search/assets"
    file_path = f"{path.dirname(__file__)}/data.txt"
    username = ""
    password = ""
    responses = []
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
        if username != "" and password != "" and base_url != "":
            assert isinstance(username, str)
            self.username = username
            assert isinstance(password, str)
            self.password = password
            assert isinstance(base_url, str)
            self.base_url = base_url

        self._repo_path = self.base_url + "service/rest/v1/search/assets"

        self.auth_info = (self.username, self.password)
    
    def _get_response(self) -> list:
        for name in self.repo_names:
            endpoint = self._repo_path + f'?repository={name}'
            response = get(endpoint, auth=self.auth_info)
            self.responses.append(response)
        return self.responses        

    def get_items(self, responses:list = []) -> list:
        if responses != []:
            assert isinstance(responses, list)
            self.responses = responses
        
        data = [r.json().get('items', []) for r in self.responses]
        
        return data
        #TODO : make package variables use self to have access when an object created!
        #TODO : break every package into isolated methods
        #TODO : typing and validation. default and search for efficiency, (pydantic).
        #TODO : use pythonic for better python-native code.
        #TODO : try to call methods within the class to get the getter data don't handle them again. 
        #TODO : you don't have to get the arguments for different parameters in every methods that's why we use class cause we already have its state.
        #TODO : add set file path.

    #     for package in data:
    #         npm_info = package.get('npm', {})
    #         package_name = npm_info.get('name')
    #         package_version = npm_info.get('version')

    #         package_size_bytes = package.get('fileSize')
    #         package_size_kb = package_size_bytes / (1024)
    #         package_last_downloaded = package.get('lastDownloaded')

    #     return package_name, package_version, package_size_kb, package_last_downloaded
    
    def get_len(self) -> int:
        p_len = len(self.repo_names)
        return p_len
