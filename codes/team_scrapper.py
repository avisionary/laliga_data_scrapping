import requests
from bs4 import BeautifulSoup
import pandas as pd

class TeamScrapper:

    def __init__(self,season,team = [],teamURL = [],squad_size = [],avg_age = [],foreigners = [],tmv = []):
        self.team = team
        self.teamURL = teamURL
        self.squad_size = squad_size
        self.avg_age = avg_age
        self.foreigners = foreigners
        self.tmv = tmv

        self.url = f"https://www.transfermarkt.us/laliga/startseite/wettbewerb/ES1/plus/?saison_id={season}"
        self.season = season

        self._headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} 

    def get_page(self,page):
        pageTree = requests.get(page, headers=self._headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        return pageSoup

    def __get_teams(self,pageSoup,teamNames,teamURLs):
        for teamName in pageSoup.findAll('td', class_ = 'hauptlink no-border-links'):
            if teamName.text != '':
                print(teamName.text)
                team_url = teamName.find('a')['href']
                teamURLs.append(team_url)

                team_name = teamName.find('a')['title']
                teamNames.append(team_name)

    def __get_team_stats(self,pageSoup,squad_size,avg_age,foreigners):
        counter = -1
        for x in pageSoup.findAll('td', class_ = 'zentriert'):
            if x.text != "" and counter <= 61:
                counter += 1
                if (counter - 1) % 3 == 0:
                    print(counter)
                    avg_age.append(x.text)
                elif (counter - 2) % 3 == 0:
                    foreigners.append(x.text)
                elif (counter - 3) % 3 == 0:
                    squad_size.append(x.text)

        squad_size.pop(0)
        avg_age.pop(0)
        foreigners.pop(0)


    def __get_tmv(self,pageSoup,tmv):
        counter = 0
        for x in pageSoup.findAll('td', class_ = 'rechts'):
            if x.text != "" and counter <= 42:
                counter += 1
                if counter % 2 == 0:
                    tmv.append(x.text)

        league_tmv = tmv.pop(0)


    def __to_df(self):
        # dictionary of lists 
        dict = {'team': self.team, 
                    'squad_size': self.squad_size, 
                    'avg_age': self.avg_age,
                    'foreigners': self.foreigners,
                    'total_market_value':self.tmv} 
        self.df = pd.DataFrame(dict)


    def use_scrapper(self):
        pageSoup = self.get_page(self.url)
        self.__get_teams(pageSoup,self.team,self.teamURL)
        self.__get_team_stats(pageSoup,self.squad_size,self.avg_age,self.foreigners)
        self.__get_tmv(pageSoup,self.tmv)
        self.__to_df()




s = TeamScrapper('2022')
s.use_scrapper()
print(s.df)


    
        
        





