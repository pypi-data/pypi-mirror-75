from typing import TYPE_CHECKING,List

from pyfootball.Helper import IObject, api_version

if TYPE_CHECKING:
    from pyfootball.League import League


class Country(IObject):
    def __init__(self,api_key : str, **kwargs):
        super().__init__(api_key)
        self._kwargs = kwargs
        self._leagues = []

    @property
    def name(self) -> str:
        if api_version == 3:
            return self._get_entry(self._kwargs,'name')
        else:
            return self._get_entry(self._kwargs,'country')
    @property
    def code(self) -> str:
        if api_version == 3:
            return self._get_entry(self._kwargs,'code')
        else:
            return self._get_entry(self._kwargs,'country_code')

    @property
    def id(self):
        return self.code

    @property
    def flag(self) -> str:
        return self._get_entry(self._kwargs,'flag')

    @property
    def leagues(self) -> List['League']:
        return self._leagues

    def add_league(self,value : 'League'):
        self._leagues.append(value)

    @staticmethod
    def endpoint():
        return "/countries"

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other : 'Country'):
        return other.code == self.code
