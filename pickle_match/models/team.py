from dataclasses import dataclass
from statistics import variance
import pandas as pd

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

    def to_df(self):
        print(f"-- Rating Variance: {self.rating_variance} --")
        team_dict = {
            "Team": [],
            "Player": [],
            "Rating": [],
        }
        for idx, team in enumerate(self.teams):
            for player in team.players:
                team_dict["Team"].append(idx)
                team_dict["Player"].append(player.name)
                team_dict["Rating"].append(player.rating)

        return pd.DataFrame.from_dict(team_dict)
