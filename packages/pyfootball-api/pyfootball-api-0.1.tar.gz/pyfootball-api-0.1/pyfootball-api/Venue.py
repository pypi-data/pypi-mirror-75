from typing import TYPE_CHECKING

from pyfootball.Helper import IObject

if TYPE_CHECKING:
    from pyfootball.Team import Team


class Venue(IObject):
    def __init__(self,api_key : str, **kwargs):
        super().__init__(api_key)
        self.kwargs = kwargs
        self._teams = []

    @property
    def id(self) -> int:
        return self.kwargs["id"]

    @property
    def name(self):
        return self.kwargs["name"]

    @property
    def address(self):
        return self.kwargs["address"]

    @property
    def city(self):
        return self.kwargs["city"]

    @property
    def capacity(self):
        return self.kwargs["capacity"]

    @property
    def surface(self):
        return self.kwargs["grass"]

    @property
    def image(self):
        return self.kwargs["image"]

    @staticmethod
    def endpoint():
        return "/venues"

    @property
    def teams(self):
        return self._teams

    def add_team(self,value : 'Team'):
        self._teams.append(value)

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return self.__repr__()