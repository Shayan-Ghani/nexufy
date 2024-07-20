from requests import get
from os import path

class Assets():
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
        # if response != []:
        #     path += [r.get('path') for r in response]            
        #     return path
                
        for response in self.get_items():
            path += [r.get('path') for r in response]
            
        # return data
        return path
    
    def get_ids(self) -> list:
        id = []
        for response in self.get_items():
            id += [f"{r.get('path')} : {r.get('id')}" for r in response]
        return id

    def npm_info(self) -> list:
        info = []
        for response in self.get_items():
            info += [f"{r.get('npm', {}).get('name')} : {r.get('npm', {}).get('version')}" for r in response]
        return info
    
    def size(self) -> list:
        f_size = []
        for response in self.get_items():
            f_size = [f"{r.get('path')} : {r.get('fileSize') / (1024)}" for r in response]

        return f_size

    def last_downloaded(self) -> dict:
        d_time = {}
        for response in self.get_items():
            for r in response:
                d_time.update({r.get('path'): r.get('lastDownloaded')})
            
        return d_time

        #TODO : typing and validation. default and search for efficiency, (pydantic).
        #TODO : changed all feature methods to process by name.
        #TODO: migrate all of the methods to work with id.
        #TODO: impel single GET as well using id.
        #TODO: isolate BULK from Single and make them inherit the base class.
        #TODO: impel component for both single and bulk.
        #TODO: impel deletion for both single and bulk.
        #TODO: use map function when possible  
    
    def get_len(self , items: list = []) -> int:
        return len(items)
    
    def get_swagger(self):
        url = self.base_url + "service/rest/swagger.json"
        swag_json = get(url).json()
        return swag_json