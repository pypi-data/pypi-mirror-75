from datetime import datetime
from typing import Dict, TYPE_CHECKING, Union, List

from pyfootball.Helper import IObject, api_version
from pyfootball.Team import Team
from pyfootball.Venue import Venue

if TYPE_CHECKING:
    from pyfootball.League import League


class LeagueSeason(IObject):
    def __init__(self,api_key : str,**kwargs):
        super().__init__(api_key)

        self.kwargs = kwargs
        self._league = None
        self._teams = None
        self._venues = None

    @property
    def venues(self):
        return self._venues

    async def get_teams(self) -> List['Team']:
        if self._teams is not None:
            return self._teams

        self._teams = []
        if api_version == 3:
            self.params = {'season':self.year,'country':self.league.country.name,'league':self.league.id}
        else:
            self.params = {'season_id':self.year,'league_id':self.league.id}
        await self.query(Team,False)
        for i in self.query_results:
            del i['team']['country']
            team = self.get_obj(Team,country=self.league.country,season=self,**i['team'])
            venue = self.get_obj(Venue,**i['venue'])
            team.venue = venue
            venue.add_team(team)
            self._teams.append(team)

        return self._teams

    @property
    def id(self) -> str:
        if self.league is not None:
            return f"{self.league.id}{self.year}"
        else:
            return f"{self.year}"

    @property
    def league(self) -> 'League':
        return self._league

    @league.setter
    def league(self, value : 'League'):
        self._league = value

    @property
    def year(self) -> int:
        if 'season' in self.kwargs.keys():
            return self.kwargs['season']
        elif 'year' in self.kwargs.keys():
            return self.kwargs['year']
        else:
            return None

    @property
    def start(self) -> Union[datetime,None]:
        key = 'start' if api_version == 3 else 'season_start'
        if key in self.kwargs.keys():
            return datetime.strptime(self.kwargs[key],'%Y-%m-%d')
        else:
            return None
    @property
    def end(self) -> Union[datetime,None]:
        key = 'end' if api_version == 3 else 'season_end'
        if key in self.kwargs.keys():
            return datetime.strptime(self.kwargs[key],'%Y-%m-%d')
        else:
            return None

    @property
    def current(self) -> bool:
        if api_version == 3:
            return self._get_entry(self.kwargs,'current')
        elif api_version ==2:
            return self._get_entry(self.kwargs,'is_current')

    @current.setter
    def current(self,value : bool):
        if api_version == 3:
            self.kwargs['current'] = value
        else:
            self.kwargs['is_current'] = value

    @property
    def has_events(self) -> bool:
        return self._get_entry(self.kwargs['coverage']['fixtures'],'events')

    @property
    def has_lineups(self) -> bool:
        return self._get_entry(self.kwargs['coverage']['fixtures'],'lineups')

    @property
    def has_statistics_fixtures(self) -> bool:
        return self._get_entry(self.kwargs['coverage']['fixtures'],'statistics_fixtures')

    @property
    def has_statistics_players(self) -> bool:
        return self._get_entry(self.kwargs['coverage']['fixtures'],'statistics_players')

    @property
    def has_standings(self) -> bool:
        return self._get_entry(self.kwargs['coverage'],'standings')

    @property
    def has_players(self) -> bool:
        return self._get_entry(self.kwargs['coverage'],'players')

    @property
    def has_top_scorers(self) -> bool:
        return self._get_entry(self.kwargs['coverage'],'top_scorers')

    @property
    def has_predictions(self) -> bool:
        return self._get_entry(self.kwargs['coverage'],'predictions')

    @property
    def has_odds(self) -> bool:
        return self._get_entry(self.kwargs['coverage'],'odds')

    @staticmethod
    def endpoint():
        if api_version == 3:
            return "/leagues/seasons"
        else:
            return "/seasons"

    def __repr__(self):
        if self.league is None:
            return f"{self.year}"
        else:
            return f"{self.league.name} - {self.year}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other : 'LeagueSeason'):
        return self.league == self.league