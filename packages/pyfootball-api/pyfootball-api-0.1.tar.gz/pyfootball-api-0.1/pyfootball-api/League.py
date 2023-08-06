from copy import deepcopy
from typing import List, TYPE_CHECKING, Union

from pyfootball.Country import Country
from pyfootball.Helper import IObject, api_version

if TYPE_CHECKING:
    from pyfootball.Season import LeagueSeason


class League(IObject):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key)

        if 'seasons' not in kwargs.keys() or 'country' not in kwargs.keys():
            raise AttributeError("You need to provide both season and country for a league")

        self._kwargs = kwargs
        self._total_market_value = None

    def get_old_league(self,year : int):
        if len([i for i in self.seasons if i.year == year]) == 0:
            raise ValueError("No league available for that year!")

        seasons = deepcopy(self._kwargs['seasons'])

        self._kwargs['seasons'] = [k for k in self._kwargs['seasons'] if k.year <= year]
        self._kwargs['seasons'][-1].current = True
        league =  League(self._api_key, **self._kwargs)
        league.current_season.league = league
        self._kwargs['seasons'] = seasons
        return league

    @property
    def id(self) -> str:
        if api_version == 3:
            return self._get_entry(self._kwargs, 'id')
        else:
            return self._get_entry(self._kwargs, 'league_id')

    @property
    def name(self) -> str:
        return self._get_entry(self._kwargs, 'name')

    @property
    def type(self) -> str:
        return self._get_entry(self._kwargs, 'type')

    @property
    def logo(self) -> str:
        return self._get_entry(self._kwargs, 'logo')

    @property
    def seasons(self) -> List['LeagueSeason']:
        return self._get_entry(self._kwargs, 'seasons')

    @property
    def country(self) -> 'Country':
        return self._get_entry(self._kwargs, 'country')

    @property
    def total_market_value(self) -> float:
        return self._total_market_value

    @total_market_value.setter
    def total_market_value(self, value : float):
        self._total_market_value = value

    @property
    def current_season(self) -> Union[None, 'LeagueSeason']:
        current_seasons = [i for i in self.seasons if i.current]
        if len(current_seasons) == 0:
            return None
        else:
            return current_seasons[0]

    @staticmethod
    def endpoint():
        return "/leagues"

    def __repr__(self):
        return f"{self.name} - {self.current_season.year}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other: 'League'):
        return self.id == other.id
