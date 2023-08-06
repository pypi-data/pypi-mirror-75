from datetime import datetime
import typing

import unidecode

from pyfootball.Helper import IObject
if typing.TYPE_CHECKING:
    from pyfootball.Team import Team


class Person(IObject):
    """
    Defines commonalities for individuals, like coaches and players
    """
    def __init__(self,api_key : str, **kwargs):
        super().__init__(api_key)
        self._kwargs = kwargs

    @property
    def id(self):
        return self._get_entry(self._kwargs,'id')

    @property
    def firstname(self) -> str:
        return unidecode.unidecode(self._get_entry(self._kwargs,'firstname'))

    @property
    def lastname(self) -> str:
        return unidecode.unidecode(self._get_entry(self._kwargs,'lastname'))

    @property
    def easy_firstname(self):
        return self.firstname.split(" ")[0]

    @property
    def easy_lastname(self):
        return self.lastname.split(" ")[-1]

    @property
    def name(self):
        return unidecode.unidecode(self._get_entry(self._kwargs,'name'))

    @property
    def birthdate(self) -> datetime:
        return datetime.strptime(self._get_entry(self._kwargs['birth'],'date'),'%Y-%m-%d')

    @property
    def age(self) -> int:
        return self._get_entry(self._kwargs,'age')

    @property
    def birthplace(self) -> str:
        return self._get_entry(self._kwargs['birth'],'place')

    @property
    def nationality(self) -> str:
        return self._get_entry(self._kwargs,'nationality')

    @property
    def height(self) -> int:
        return self._get_entry(self._kwargs,'height')

    @property
    def weight(self) -> float:
        return self._get_entry(self._kwargs,'weight')

    @property
    def team(self) -> 'Team':
        return self._get_entry(self._kwargs,'team')

    @staticmethod
    def endpoint():
        raise NotImplementedError()

    def __repr__(self):
        return f"{self.lastname} {self.firstname} - {self.team}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other : 'Person'):
        return self.id == other.id
