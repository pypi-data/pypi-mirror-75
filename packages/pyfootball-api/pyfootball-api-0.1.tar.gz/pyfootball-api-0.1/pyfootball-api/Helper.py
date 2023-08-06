import json
from typing import Dict, Union, List, Type, TypeVar, Generic

import aiohttp
from aiohttp import ClientResponse

api_dict = {
    2: "https://v2.api-football.com",
    3: "https://v3.football.api-sports.io"
}

api_version=3

class HTTP404Error(Exception):
    def __init__(self,msg:str):
        self._msg = msg

T = TypeVar('T')

class ObjectManager:
    _instance = None

    @staticmethod
    def inst() -> 'ObjectManager':
        if ObjectManager._instance == None:
            ObjectManager()

        return ObjectManager._instance

    def __init__(self):
        if ObjectManager._instance != None:
            raise Exception("Singleton, you can't instantiate this class")
        else:
            ObjectManager._instance = self

        self.obj_dict = {}

    def get_obj(self,obj_model : Generic[T],api_key, **kwargs) -> Generic[T]:
        try:
            data_list : List[Generic[T]] = self.obj_dict[obj_model]
            return [i for i in data_list if i.id == kwargs['id']][0]

        except (KeyError,IndexError) as e:
            new_obj = obj_model(api_key,**kwargs)
            if obj_model in self.obj_dict.keys():
                self.obj_dict[obj_model].append(new_obj)
            else:
                self.obj_dict[obj_model] = [new_obj]

            return new_obj

class IObject(Generic[T]):
    """
    IObject is the basic data type for any Data class in The API. It gives you the basic capabilities fo perform queries
    to football api
    """
    def __init__(self,api_key : str):
        self._params = None
        self._api_key = api_key
        self._headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        }
        self._raw_response = None
        self._response_text = None
        self._url = None

    @staticmethod
    def endpoint():
        raise NotImplementedError("You need to implement the static endpoint property for this object!")

    @property
    def id(self):
        raise NotImplementedError("You need to implement the ID property for this object")

    @property
    def params(self) -> Dict[str,Union[str,int]]:
        """
        Parameters for the request. You need to set this through the setter if you want to use params
        """
        return self._params

    @params.setter
    def params(self, value : Dict[str,Union[str,int]]):
        """
        Param setter for the request.
        :value: Value to be set
        """
        self._params = value

    @property
    def query_results(self) -> List:
        """
        Returns the raw response list after the query
        """
        if api_version ==3:
            return self.response_dict['response']
        elif api_version == 2:
            return [val for key,val in self.response_dict['api'].items() if key !='results'][0]

    @property
    def query_get(self) -> str:
        """
        Endpoint used in the query
        """
        return self.response_dict['get']

    @property
    def query_parameters(self) -> List:
        """
        Lists the query parameters
        """
        return self.response_dict['parameters']

    @property
    def raw_response(self) -> ClientResponse:
        """
        Raw response object from aiohttp
        """
        return self._raw_response

    @property
    def response_text(self) -> str:
        """
        Raw response text from accessing self.raw_response.read()
        """
        return self._response_text

    @property
    def response_dict(self) -> Dict:
        """
        Full response dict. Converted from self.response_text
        """
        return json.loads(self.response_text)

    @property
    def url(self):
        return self._url

    def _get_entry(self,target_dict : Dict, key : str):
        if key in target_dict.keys():
            return target_dict[key]
        else:
            return None

    def get_obj(self,obj_model : Generic[T], **kwargs) -> Generic[T]:
        return ObjectManager.inst().get_obj(obj_model,self._api_key,**kwargs)

    async def query(self,obj : 'IObject[T]', ret_obj = True):
        self._url = api_dict[api_version] + obj.endpoint()
        async with aiohttp.ClientSession() as session:
            async with session.request("GET",self._url,headers=self._headers,params=self.params) as self._raw_response:
                if self._raw_response.status != 200:
                    raise HTTP404Error(f"{self._url} get returned {self._raw_response.status}")

                self._response_text = await self._raw_response.read()

        if ret_obj:
            try:
                return [obj(self._api_key,**i) for i in self.query_results]
            except TypeError:
                return [obj(self._api_key,year=i) for i in self.query_results]

    def __eq__(self, other):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __hash__(self):
        return hash("Object"*len(self.__repr__()))



