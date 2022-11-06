import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re

from team_scrapper import TeamScrapper

class PlayerScrapper:
    """
    A class to scrape La Liga players data and stores into a dataframe
    
    ----------
    Attributes
    ----------
    season:str
        Gets the season for which data needs to be collected
    players: list
        A list to append player names
    teamURL: list
        A list to append team URLs
    age: list
        A list to append age of each player
    dob: list
        A list to append date of birth of players
    shirt_number: list
        A list to append shirt number of the players
    foot: list
        A list to append strong foot of the players
    mv: list
        A list to append market value of the players
    joined: list
        A list to append date of joining of players
    contract: list
        A list to append date of contract of players

    -------
    Methods
    -------
    set_url: Changes URL to go the detailed version of every player's table
    __get_players: Uses the HTML tag td and class posrela to get all player names and their positions
    __get_player_stats: Uses the HTML tag td and class zentriert to get all player stats
    __get_mv: Uses the HTML tag td and class rechts hauptlink to get all player market value
    __to_df : Creates a dictonary of all the appended lists and turns it into a pandas DF
    __to_csv : Saves the pandas DF to a csv file in the specified location
    use_player_scrapper : Calls the methods in a desired order to use the scrapper
    
    """

    def __init__(self,season):
        self.season = season

        self.players = []
        self.dob = []
        self.age = []
        self.mv = []
        self.position = []
        self.shirt_number  = []
        self.height = []
        self.foot = []
        self.joined = []
        self.contract = []
        self.teams = []

        self.team_scrapper = TeamScrapper(season=season)
        self._header = self.team_scrapper._headers

        self.team = []
        self.teamURL = []

        pageSoup = self.team_scrapper.get_page(self.team_scrapper.url)
        self.team_scrapper.get_teams(pageSoup,self.team,self.teamURL)


    def set_url(self,teamURL):
        '''Takes in the URL, returns the string into a desired format'''
        temp = teamURL
        temp = f"https://www.transfermarkt.us{temp}/plus/1"
        #print(temp)
        temp = temp.replace("startseite","kader")
        return temp


    def get_players(self,pageSoup,players,position):
        '''Takes in the HTML of the URL, appends player name and position to the specific list'''
        counter = 0
        for test in pageSoup.findAll('td', class_ = "posrela"):
            for row in test.findAll("tr"):
                counter += 1
                if counter % 2 == 0:
                    pos = (row.find('td').text)
                    pos = pos.strip()
                    pos = pos.replace("\n","")
                    position.append(pos)

                if counter % 2 != 0:
                    player = (row.find('a').text)
                    player = player.strip()
                    player = player.replace("\n","")
                    players.append(player)


    def get_player_stats(self,pageSoup,shirt_number,dob,age,height,foot,joined,contract):
        '''Takes in the HTML of the URL, appends player stats to desired lists'''
        counter = 0
        for x in pageSoup.findAll('table',class_ = "items"):
            for test in x.findAll('td', class_ = "zentriert"):

                    counter += 1

                    if (counter - 1) % 8 ==0 :
                        d = test.text
                        shirt_number.append(d)

                    if (counter - 2) % 8 ==0 :
                        d = test.text
                        reg = re.compile("(.+).\((\d+)\)")
                        temp = re.findall(reg,d)
                        
                        dob.append(temp[0][0])
                        age.append(temp[0][1])

                    if (counter - 4) % 8 ==0 :
                        d = test.text
                        d = d.replace(",",".")
                        height.append(d)

                    if (counter - 5) % 8 ==0 :
                        d = test.text
                        foot.append(d)

                    if (counter - 6) % 8 ==0 :
                        d = test.text
                        joined.append(d)

                    if (counter - 8) % 8 ==0 :
                        d = test.text
                        contract.append(d)


    
    def get_mv(self,pageSoup,mv,teams,team):
        '''Takes in the HTML of the URL, appends market value of the player to desired list'''
        for test in pageSoup.findAll('td',class_ = "rechts hauptlink"):
            if test != "":
                d = test.text
                mv.append(d)
                teams.append(team)



    def to_df(self):
        '''Takes in the HTML of the URl, appends team name and URL to the specific list'''
        # dictionary of lists 
        dict = {"player" : self.players,
                    'position' : self.position,
                    'team': self.teams, 
                    'shirt_number' : self.shirt_number,
                    'dob' : self.dob,
                    'age' : self.age,
                    'height' : self.height,
                    'strong_foot' : self.foot,
                    'date_joined' : self.joined,
                    'date_contract' : self.contract,
                    'market_value' : self.mv} 
        self.players_df = pd.DataFrame(dict)




    def to_csv(self,location):
        '''Takes in a location, and saves the dataframe to that location'''
        self.players_df.to_csv(location,index = False)




    def use_player_scrapper(self):
        '''Calls all the methods in the desired order, call this function on the class instantiation'''
        for i in range(len(self.teamURL)):
            team = self.team[i]
            url = self.teamURL[i]
            url2 = self.set_url(url)
            pageSoup = self.team_scrapper.get_page(url2)
            self.get_players(pageSoup,self.players,self.position)
            self.get_player_stats(pageSoup,self.shirt_number,self.dob,self.age,self.height,self.foot,self.joined,self.contract)
            self.get_mv(pageSoup,self.mv,self.teams,team)
        self.to_df()
        self.to_csv(location="./data/players.csv")