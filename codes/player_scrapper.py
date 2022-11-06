import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re

from team_scrapper import TeamScrapper

class PlayerScrapper:

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
        temp = teamURL
        temp = f"https://www.transfermarkt.us{temp}/plus/1"
        #print(temp)
        temp = temp.replace("startseite","kader")
        return temp


    def __get_players(self,pageSoup,players,position):
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


    def __get_player_stats(self,pageSoup,shirt_number,dob,age,height,foot,joined,contract):
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


    
    def __get_mv(self,pageSoup,mv,teams,team):
        for test in pageSoup.findAll('td',class_ = "rechts hauptlink"):
            if test != "":
                d = test.text
                mv.append(d)
                teams.append(team)



    def __to_df(self):
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




    def __to_csv(self,location):
        self.players_df.to_csv(location,index = False)




    def use_player_scrapper(self):
        for i in range(len(self.teamURL)):
            team = self.team[i]
            url = self.teamURL[i]
            url2 = self.set_url(url)
            pageSoup = self.team_scrapper.get_page(url2)
            self.__get_players(pageSoup,self.players,self.position)
            self.__get_player_stats(pageSoup,self.shirt_number,self.dob,self.age,self.height,self.foot,self.joined,self.contract)
            self.__get_mv(pageSoup,self.mv,self.teams,team)
        self.__to_df()
        self.__to_csv(location="./data/players.csv")