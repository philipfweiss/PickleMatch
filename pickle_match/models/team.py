from dataclasses import dataclass
from statistics import variance
from pickle_match.models.player import Player
from typing import List

@dataclass
class Team:
    NUM_PLAYERS = 4
    players: List[Player]

    @property
    def average_rating(self):
        return sum(player.rating for player in self.players) / self.NUM_PLAYERS

@dataclass
class Teams:
    teams: List[Team]

    def __iter__(self):
        for team in self.teams:
            yield team 

    @property 
    def rating_variance(self):
        return variance(team.average_rating for team in self.teams)

    def print_teams(self):
        print(f" ~~ Created {len(self.teams)} Teams ~~")
        print(f"Rating Variance: {self.rating_variance } ~~")
        print("")
    
        for idx, team in enumerate(self.teams):
            print(f"----- Team {idx+1} -----")
            for player in team.players:
                print(f" * {player.name}")
            print("")
