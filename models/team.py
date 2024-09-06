from dataclasses import dataclass
from statistics import variance
from PickleMatch.models.player import Player
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
