from dataclasses import dataclass
from pickle_match.models.pair import Pair
from typing import List
import pandas as pd

@dataclass
class Match:
    first: Pair
    second: Pair

@dataclass
class Matches:
    matches: List[Match]

    def __iter__(self):
        for match in self.matches:
            yield match 

    def to_df(self, round_no):
        title = f"Round {round_no} pairings:"
        team_dict = {
           title: [],
            "---": [],
        }
        for match in self.matches:
            first_pair, second_pair = match.first, match.second
            team_dict[title].append(f"{first_pair.first.name} and {first_pair.second.name}")
            team_dict["---"].append(f"{second_pair.first.name} and {second_pair.second.name}")

        dataframe = pd.DataFrame.from_dict(team_dict)
        dataframe.style.set_caption(f"Round {round_no} pairings")
        return dataframe
