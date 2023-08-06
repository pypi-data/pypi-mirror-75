from copy import deepcopy
from datetime import datetime
from typing import TYPE_CHECKING, List
import re

from robobrowser import RoboBrowser

from pyfootball.Helper import IObject
from pyfootball.Person import Person
from pyfootball.League import League
from pyfootball.Venue import Venue

if TYPE_CHECKING:
    from pyfootball.Season import LeagueSeason


class Team(IObject):
    def __init__(self,api_key : str, **kwargs):
        super().__init__(api_key)
        self.kwargs = kwargs
        self._venue = None
        self._players = None
        self._coach = None
        self._market_value = None

    async def get_players(self,season : int= None) -> List['Player']:
        """
        if self._players is not None:
            return self._players
        """

        self.params = {'team':self.id}

        if season is None:
            season_year = self.season.year

        else:
            season_year = self.season.year

        self.params['season'] = season_year
        self._players = []
        for i in range(1,21):
            self.params['page'] = i
            await self.query(Player,False)

            if len(self.query_results) == 0:
                break

            for i in self.query_results:
                data_dict = i
                data_dict['team'] = self
                data_dict['season_year'] = season_year
                self._players.append(Player(self._api_key,**data_dict))

        return self._players

    def get_team_value(self) -> float:
        if self._market_value is not None:
            return self._market_value

        browser = RoboBrowser(history=True,user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')
        base_url = 'https://www.transfermarkt.com'

        browser.open(base_url)
        form = browser.get_form(id='schnellsuche')
        form['query'].value = self.name
        browser.submit_form(form)
        data_list = []
        for i in browser.find_all('a'):
            try:
                if i['class'] == ['vereinprofil_tooltip']:
                    data_list.append(i)
            except:
                pass

        browser.open(base_url + data_list[0]['href'])
        market_value_entry = []
        for i in browser.find_all('div'):
            try:
                if i['class'] == ['dataMarktwert']:
                    market_value_entry.append(i)
            except:
                pass
        self._market_value = float(re.findall(r'\d+\.*\d*',market_value_entry[0].text.strip())[0])
        return self._market_value

    async def get_coach(self) -> 'Coach':
        if self._coach is not None:
            return self._coach

        self.params = {'team':self.id}
        await self.query(Coach,False)
        current_coaches = [i for i in self.response_dict['response'] if i['career'][0]['end'] is None]
        if len(current_coaches) > 1:
            coach = None
            for i in current_coaches:
                if coach is None:
                    coach = i
                else:
                    coach_start_date = datetime.strptime(coach['career'][0]['start'],'%Y-%m-%d')
                    i_start_date = datetime.strptime(i['career'][0]['start'],'%Y-%m-%d')

                    if i_start_date > coach_start_date:
                        coach = i
        else:
            coach = current_coaches[0]
        del coach['team']
        self._coach = self.get_obj(Coach,team=self,**coach)
        return self._coach

    @property
    def id(self) -> int:
        return self.kwargs["id"]
    
    @property
    def name(self):
        return self.kwargs["name"]

    @property
    def country(self):
        return self.kwargs["country"]

    @property
    def founded(self):
        return self.kwargs["founded"]

    @property
    def national(self):
        return self.kwargs["national"]
    
    @property
    def logo(self):
        return self.kwargs["logo"]

    @property
    def season(self) -> 'LeagueSeason':
        return self.kwargs["season"]

    @season.setter
    def season(self,value : 'LeagueSeason'):
        self.kwargs['season'] = value

    @property
    def league(self) -> 'League':
        return self.season.league

    @property
    def venue(self) -> 'Venue':
        return self._venue

    @venue.setter
    def venue(self, value : 'Venue'):
        self._venue = value

    @staticmethod
    def endpoint():
        return "/teams"

    def __repr__(self):
        return f"{self.name} - {self.league}"

    def __str__(self):
        return self.__repr__()

class PlayerHistory(IObject):
    def __init__(self,api_key : str, **kwargs):
        super().__init__(api_key)
        self._kwargs = kwargs

    @staticmethod
    def endpoint():
        return "/players/seasons"

class Player(Person):
    def __init__(self, api_key: str, **kwargs):
        if 'team' not in kwargs.keys():
            raise AttributeError("Any Player instance needs to have an associated Team instance.")

        super().__init__(api_key,team=kwargs['team'], **kwargs['player'])

        self._league_stats = {}
        stat_dict = kwargs['statistics']
        self._teams = None
        self._market_value = None
        self._image_url = None



        for i in stat_dict:
            del i['league']['country']
            del i['league']['season']
            league = self.get_obj(League,seasons = self.team.season,country = self.team.league.country,**i['league'])
            i['league'] = league
            i['player'] = self
            self._league_stats[league.name] = self.get_obj(PlayerStat,**i)

        self._kwargs['playerstat'] = PlayerStat.aggregate_object(list(self._league_stats.values()))

    async def get_team_history(self) -> List[Team]:
        if self._teams is not None:
            return self._teams

        await self.query(PlayerHistory,False)
        season_list = self.response_dict['response']
        self._teams = []
        for season_year in season_list[14:]:
            self.params = {'id':self.id,'season':season_year}
            await self.query(Player,False)
            if len(self.response_dict['response']) == 0:
                continue

            data_dict = self.response_dict['response'][0]['statistics'][0]['league']
            league = self.get_obj(League,**data_dict)

            if league.id is None:
                continue

            try:
                league = league.get_old_league(season_year)
            except:
                pass
            team_info = self.response_dict['response'][0]['statistics'][0]['team']

            self.params = {'id':team_info['id'],'season':season_year,'league':league.id}
            await self.query(Team,False)

            self.response_dict['response'][0]['team']['country']  = league.country

            team_template : Team= self.get_obj(Team,**self.response_dict['response'][0]['team'])
            kwargs = team_template.kwargs
            team : Team= Team(self._api_key,**kwargs)
            team.season = league.current_season
            venue = self.get_obj(Venue,**self.response_dict['response'][0]['venue'])
            team.venue = venue
            venue.add_team(team)

            self._teams.append(team)

        return self._teams

    def get_market_value(self) -> float:
        if self._market_value is None:
            self.crawl_tm()

        return self._market_value

    def get_player_image(self):
        if self._image_url is None:
            self.crawl_tm()

        return self._image_url

    def crawl_tm(self):
        base_url = 'https://www.transfermarkt.com'
        browser = RoboBrowser(history=True,user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')
        browser.open(base_url)
        form = browser.get_form(id='schnellsuche')
        form['query'].value = f"{self.firstname.split(' ')[0]} {self.name.split(' ')[-1]}"

        browser.submit_form(form)
        data_list = []
        for i in browser.find_all('a'):
            try:
                if i['class'] == ['spielprofil_tooltip']:
                    data_list.append(i)
            except:
                pass
        try:
            browser.open(base_url + data_list[0]['href'])
        except:
            print(browser.url)
            self._market_value = 0
            return self._market_value

        market_value_entry = []
        for i in browser.find_all('div'):
            try:
                if i['class'] == ['right-td']:
                    market_value_entry.append(i)
                if i['class'] == ['dataBild']:
                    self._image_url = i.contents[1]['src']
            except:
                pass
        try:
            if "m" in market_value_entry[0].string:
                self._market_value = float(re.findall(r'\d+\.*\d*',market_value_entry[0].string.strip())[0])
            if "Th" in market_value_entry[0].string:
                self._market_value = float(re.findall(r'\d+\.*\d*',market_value_entry[0].string.strip())[0])/1000
        except:
            print(browser.url)
            return 0

    @property
    def playerstat(self) -> 'PlayerStat':
        return self._get_entry(self._kwargs, 'playerstat')

    @staticmethod
    def endpoint():
        return "/players"

    @property
    def league_stats(self) -> List['PlayerStat']:
        return self._league_stats


class IStatObj(IObject):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key)
        self._kwargs = kwargs

        if 'playerstat' not in kwargs.keys():
            raise AttributeError("Any lower stat model needs to have an associated playerstat object")

    @property
    def playerstat(self) -> 'PlayerStat':
        return self._get_entry(self._kwargs, 'playerstat')

    def __add__(self, other):
        data_dict = {}
        for key in self._kwargs.keys():
            if isinstance(self._kwargs[key],int) or isinstance(self._kwargs[key],float) or self._kwargs[key] is None:
                if self._kwargs[key] is None:
                    data_dict[key] = other._kwargs[key]
                elif other._kwargs[key] is None:
                    data_dict[key] = self._kwargs[key]
                else:
                    data_dict[key] = self._kwargs[key] + other._kwargs[key]

        data_dict['playerstat'] = self._kwargs['playerstat']
        return type(self)(self._api_key,**data_dict)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


class GameStats(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def appearences(self) -> int:
        return self._get_entry(self._kwargs, 'appearences')

    @property
    def lineups(self) -> int:
        return self._get_entry(self._kwargs, 'lineups')

    @property
    def minutes(self) -> int:
        return self._get_entry(self._kwargs, 'minutes')

    @property
    def number(self) -> int:
        return self._get_entry(self._kwargs, 'number')

    @property
    def position(self) -> str:
        return self._get_entry(self._kwargs, 'position')

    @property
    def rating(self) -> float:
        return self._get_entry(self._kwargs, 'rating')

    @property
    def captain(self) -> bool:
        return self._get_entry(self._kwargs, 'captain')

    def __repr__(self):
        return f"App: {self.appearences} -> {self.minutes} minutes"

    def __str__(self):
        return self.__repr__()



class Substitutes(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def subin(self) -> int:
        return self._get_entry(self._kwargs, 'in')

    @property
    def subout(self) -> int:
        return self._get_entry(self._kwargs, 'out')

    def __repr__(self):
        return f"Subin: {self.subin}, subout {self.subout}"

    def __str__(self):
        return self.__repr__()


class Shots(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def total(self) -> int:
        return self._get_entry(self._kwargs, 'total')

    @property
    def on(self) -> int:
        return self._get_entry(self._kwargs, 'on')

    def __repr__(self):
        return f"Total: {self.total}, on target {self.on}"

    def __str__(self):
        return self.__repr__()


class Goals(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def total(self) -> int:
        return self._get_entry(self._kwargs, 'total')

    @property
    def conceded(self) -> int:
        return self._get_entry(self._kwargs, 'conceded')

    @property
    def assists(self) -> int:
        return self._get_entry(self._kwargs, 'assists')

    def __repr__(self):
        return f"Total: {self.total}, conceded {self.conceded}, assists {self.assists}"

    def __str__(self):
        return self.__repr__()


class Passes(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def total(self):
        return self._get_entry(self._kwargs, 'total')

    @property
    def key(self):
        return self._get_entry(self._kwargs, 'key')

    @property
    def accuracy(self):
        return self._get_entry(self._kwargs, 'accuracy')

    def __repr__(self):
        return f"Total: {self.total}, key {self.key}, accuracy {self.accuracy}"

    def __str__(self):
        return self.__repr__()


class Tackles(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def total(self):
        return self._get_entry(self._kwargs, 'total')

    @property
    def blocks(self):
        return self._get_entry(self._kwargs, 'blocks')

    @property
    def interceptions(self):
        return self._get_entry(self._kwargs, 'interceptions')


class Duels(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def total(self):
        return self._get_entry(self._kwargs, 'total')

    @property
    def won(self):
        return self._get_entry(self._kwargs, 'won')


class Dribbles(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def attempts(self):
        return self._get_entry(self._kwargs, 'attempts')

    @property
    def success(self):
        return self._get_entry(self._kwargs, 'success')

    @property
    def past(self):
        return self._get_entry(self._kwargs, 'past')


class Fouls(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def drawn(self):
        return self._get_entry(self._kwargs, 'drawn')

    @property
    def committed(self):
        return self._get_entry(self._kwargs, 'committed')


class Cards(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def yellow(self):
        return self._get_entry(self._kwargs, 'yellow')

    @property
    def yellowred(self):
        return self._get_entry(self._kwargs, 'yellowred')

    @property
    def red(self):
        return self._get_entry(self._kwargs, 'red')


class Penalty(IStatObj):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)

    @property
    def won(self):
        return self._get_entry(self._kwargs, 'won')

    @property
    def commited(self):
        return self._get_entry(self._kwargs, 'commited')

    @property
    def scored(self):
        return self._get_entry(self._kwargs, 'scored')

    @property
    def missed(self):
        return self._get_entry(self._kwargs, 'missed')

    @property
    def saved(self):
        return self._get_entry(self._kwargs, 'saved')


class PlayerStat(IObject):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key)
        self._kwargs = kwargs

        if 'player' not in kwargs.keys():
            raise AttributeError("Any Player stat needs to have an associated player")

        if 'aggregated_obj' not in kwargs.keys() or ('aggregated_obj' in kwargs.keys() and not kwargs['aggregated_obj']):
            self._gamestats = GameStats(api_key, playerstat = self, **kwargs['games'])
            self._substitutes = Substitutes(api_key, playerstat = self, **kwargs['substitutes'])
            self._shots = Shots(api_key, playerstat = self, **kwargs['shots'])
            self._goals = Goals(api_key, playerstat = self, **kwargs['goals'])
            self._passes = Passes(api_key, playerstat = self, **kwargs['passes'])
            self._tackles = Tackles(api_key, playerstat = self, **kwargs['tackles'])
            self._duels = Duels(api_key, playerstat = self, **kwargs['duels'])
            self._dribbles = Dribbles(api_key, playerstat = self, **kwargs['dribbles'])
            self._fouls = Fouls(api_key, playerstat = self, **kwargs['fouls'])
            self._cards = Cards(api_key, playerstat = self, **kwargs['cards'])
            self._penalty = Penalty(api_key, playerstat = self, **kwargs['penalty'])
            self._aggregated_obj = False
        else:
            self._aggregated_obj = True

    @staticmethod
    def aggregate_object(playerstat_list : List['PlayerStat']):
        obj = PlayerStat(playerstat_list[0]._api_key,aggregated_obj=True,player=playerstat_list[0].player)
        obj._gamestats = sum([i.gamestats for i in playerstat_list])
        obj._substitutes = sum([i.substitutes for i in playerstat_list])
        obj._shots = sum([i.shots for i in playerstat_list])
        obj._goals = sum([i.goals for i in playerstat_list])
        obj._passes = sum([i.passes for i in playerstat_list])
        obj._tackles = sum([i.tackles for i in playerstat_list])
        obj._duels = sum([i.duels for i in playerstat_list])
        obj._dribbles = sum([i.dribbles for i in playerstat_list])
        obj._fouls = sum([i.fouls for i in playerstat_list])
        obj._cards = sum([i.cards for i in playerstat_list])
        obj._penalty = sum([i.penalty for i in playerstat_list])

        obj._gamestats._kwargs['playerstat'] = obj
        obj._substitutes._kwargs['playerstat'] = obj
        obj._shots._kwargs['playerstat'] = obj
        obj._goals._kwargs['playerstat'] = obj
        obj._passes._kwargs['playerstat'] = obj
        obj._tackles._kwargs['playerstat'] = obj
        obj._duels._kwargs['playerstat'] = obj
        obj._dribbles._kwargs['playerstat'] = obj
        obj._fouls._kwargs['playerstat'] = obj
        obj._cards._kwargs['playerstat'] = obj
        obj._penalty._kwargs['playerstat'] = obj
        return obj

    @property
    def stat_list(self):
        return [
            self._gamestats,
            self._substitutes,
            self._shots,
            self._goals,
            self._passes,
            self._tackles,
            self._duels,
            self._dribbles,
            self._fouls,
            self._cards,
            self._penalty
        ]

    @property
    def aggregated_obj(self):
        return self._aggregated_obj

    @property
    def league(self):
        return self._get_entry(self._kwargs,'league')

    @property
    def gamestats(self) -> GameStats:
        return self._gamestats

    @property
    def substitutes(self) -> Substitutes:
        return self._substitutes

    @property
    def shots(self) -> Shots:
        return self._shots

    @property
    def goals(self) -> Goals:
        return self._goals

    @property
    def passes(self) -> Passes:
        return self._passes

    @property
    def tackles(self) -> Tackles:
        return self._tackles

    @property
    def duels(self) -> Duels:
        return self._duels

    @property
    def dribbles(self) -> Dribbles:
        return self._dribbles

    @property
    def fouls(self) -> Fouls:
        return self._fouls

    @property
    def cards(self) -> Cards:
        return self._cards

    @property
    def penalty(self) -> Penalty:
        return self._penalty

    @property
    def player(self) -> 'Player':
        return self._get_entry(self._kwargs, 'player')

    @property
    def id(self):
        return self.player.id

    def __repr__(self):
        return f"Playerstats {self.player} - {self.league}"

    def __str__(self):
        return self.__repr__()

class Coach(Person):
    def __init__(self, api_key: str, **kwargs):
        if 'team' not in kwargs.keys():
            raise AttributeError("Any Coach instance needs to have an associated Team instance.")

        super().__init__(api_key,**kwargs)

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def endpoint():
        return "/coachs"
