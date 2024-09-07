from dataclasses import dataclass
from statistics import variance
import pandas as pd

from pickle_match.models.player import Player
from pickle_match.models.pair import Pair
from pickle_match.models.constraint import Constraint

from typing import List

@dataclass
class Team:
    players: List[Player]
    team_id: int

    @property
    def average_rating(self):
        return sum(player.rating for player in self.players) / 4

    @property
    def pairs(self):
        a, b, c, d = self.players
        return [
            Pair(first=a, second=b, team_id=self.team_id), # Round 1 
            Pair(first=c, second=d, team_id=self.team_id),
            Pair(first=a, second=c, team_id=self.team_id), # Round 2
            Pair(first=b, second=d, team_id=self.team_id),
            Pair(first=a, second=d, team_id=self.team_id), # Round 3
            Pair(first=b, second=c, team_id=self.team_id),
        ]
    

    def default_constraints(self, pair):
        return [
            Constraint(
                pair=pair,
                denied_pair=deny
            )
            for deny in self.pairs
        ]

@dataclass
class Teams:
    teams: List[Team]

    def __iter__(self):
        for team in self.teams:
            yield team 

    @property
    def num_teams(self):
        return len(self.teams)

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
        for team in self.teams:
            for player in team.players:
                team_dict["Team"].append(team.team_id)
                team_dict["Player"].append(player.name)
                team_dict["Rating"].append(player.rating)

        return pd.DataFrame.from_dict(team_dict)
    