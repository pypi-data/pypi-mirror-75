import asyncio
from copy import deepcopy
from typing import List

from pyfootball.Country import Country
from pyfootball.Helper import IObject, ObjectManager, api_version
from pyfootball.League import League
from pyfootball.Season import LeagueSeason


class FootballApi(IObject):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self._countries = None
        self._league_seasons = None
        self._leagues = None

    @property
    def countries(self):
        return self._countries

    @property
    def league_seasons(self):
        return self._league_seasons

    @property
    def leagues(self) -> List[League]:
        return self._leagues

    @property
    def top_4_leagues(self) -> List[League]:
        countries = [i for i in self.countries if i.name in ["France", "Germany", "England", "Spain","Italy"]]
        return [i for i in self.leagues if
                i.name in ['Bundesliga 1','Primera Division', 'Serie A','Premier League'] and i.country in countries]

    async def load_leagues(self):
        if self._leagues is not None:
            return
        await self.query(League, False)
        self._countries = []
        self._leagues = []
        self._league_seasons = []
        result = deepcopy(self.query_results)

        for i in result:
            if api_version == 3:
                country = self.get_obj(Country, **i['country'])
            elif api_version == 2:
                country_keys = ['country','country_code','flag']
                data_dict = {}
                for key in country_keys:
                    data_dict[key] = i[key]
                    del i[key]
                country = self.get_obj(Country,**data_dict)
            else:
                continue

            if api_version == 3:
                league_season = [self.get_obj(LeagueSeason, **j) for j in i['seasons']]
            elif api_version == 2 and i['name'] not in [m.name for m in self._leagues]:
                league_season = []
                season_keys = ['season','season_start','season_end','is_current','coverage']
                for season in [l for l in result if l['name'] == i['name']]:
                    data_dict = {}
                    for key in season_keys:
                        data_dict[key] = season[key]
                    league_season.append(self.get_obj(LeagueSeason,**data_dict))

                for key in season_keys:
                    del i[key]
            else:
                continue

            if api_version == 3:
                data_dict = i['league']
            else:
                data_dict = i
            data_dict['seasons'] = league_season
            data_dict['country'] = country
            league = self.get_obj(League, **data_dict)

            for j in league_season:
                j.league = league

            if country not in self._countries:
                self._countries.append(country)
            else:
                country = self._countries[self._countries.index(country)]

            country.add_league(league)

            self._leagues.append(league)
            if league_season is not None:
                self._league_seasons += [i for i in league_season if i not in self._league_seasons]
