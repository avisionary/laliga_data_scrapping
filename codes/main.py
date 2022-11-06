from team_scrapper import TeamScrapper
from player_scrapper import PlayerScrapper

def teams():
    # using team scrapper
    team_class = TeamScrapper('2022')
    team_class.use_team_scrapper()


def players():
    # using player scrapper
    player_class = PlayerScrapper('2022')
    player_class.use_player_scrapper()


def main():
    # call methods to run scrapper pipelines
    teams()
    players()

if __name__ == "__main__":
    main()