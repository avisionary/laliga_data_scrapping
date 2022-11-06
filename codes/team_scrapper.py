import requests
from bs4 import BeautifulSoup
import pandas as pd

class TeamScrapper:
    """
    A class to scrape La Liga team data and store into a dataframe
    
    ----------
    Attributes
    ----------
    season:str
        Gets the season for which data needs to be collected
    team: list
        A list to append team names
    teamURL: list
        A list to append team URLs
    squad_size: list
        A list to append squad size of each team
    avg_age: list
        A list to append average age
    foreigners: list
        A list to append number of foreigners in a team
    tmv: list
        A list to append total market values of teams
    
    
    -------
    Methods
    -------
    
    get_page: Uses BeautifulSoup to get HTML page of the URL
    get_teams: Uses the HTML tag td and class hauptlink no-border-links to get all team names
    __get_team_stats: Uses the HTML tag td and class zentriert to get all team stats
    __get_tmv: Uses the HTML tag td and class rechts to get all team stats
    __to_df : Creates a dictonary of all the appended lists and turns it into a pandas DF
    __to_csv : Saves the pandas DF to a csv file in the specified location
    use_team_scrapper : Calls the methods in a desired order to use the scrapper
    
    """

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
        '''Takes in the URL, returns HTMl of that URL'''
        pageTree = requests.get(page, headers=self._headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        return pageSoup

    def get_teams(self,pageSoup,teamNames,teamURLs):
        '''Takes in the HTML of the URl, appends team name and URL to the specific list'''
        for teamName in pageSoup.findAll('td', class_ = 'hauptlink no-border-links'):
            if teamName.text != '':
                print(teamName.text)
                team_url = teamName.find('a')['href']
                teamURLs.append(team_url)

                team_name = teamName.find('a')['title']
                teamNames.append(team_name)

    def __get_team_stats(self,pageSoup,squad_size,avg_age,foreigners):
        '''Takes in the HTML of the URl, appends team squad size, average age, number of foreigners to the specific list'''
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
        '''Takes in the HTML of the URl, appends total market value to the specific list'''
        counter = 0
        for x in pageSoup.findAll('td', class_ = 'rechts'):
            if x.text != "" and counter <= 42:
                counter += 1
                if counter % 2 == 0:
                    tmv.append(x.text)

        league_tmv = tmv.pop(0)


    def __to_df(self):
        '''Takes in all the list elements, and turns them to a pandas dataframe'''
        # dictionary of lists 
        dict = {'team': self.team, 
                    'squad_size': self.squad_size, 
                    'avg_age': self.avg_age,
                    'foreigners': self.foreigners,
                    'total_market_value':self.tmv} 
        self.teams_df = pd.DataFrame(dict)


    def __to_csv(self,location):
        '''Takes in a location, and saves the dataframe to that location'''
        self.teams_df.to_csv(location,index = False)


    def use_team_scrapper(self):
        '''Calls all the methods in the desired order, call this function on the class instantiation'''
        pageSoup = self.get_page(self.url)
        self.get_teams(pageSoup,self.team,self.teamURL)
        self.__get_team_stats(pageSoup,self.squad_size,self.avg_age,self.foreigners)
        self.__get_tmv(pageSoup,self.tmv)
        self.__to_df()
        self.__to_csv(location="./data/teams.csv")
