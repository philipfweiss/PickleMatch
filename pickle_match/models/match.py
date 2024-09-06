from dataclasses import dataclass
from pickle_match.models.pair import Pair
from typing import List
from collections import Counter
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
            team_dict[title].append(f"(Team {first_pair.team_id}) {first_pair.first.name} and {first_pair.second.name}")
            team_dict["---"].append(f"(Team {second_pair.team_id}) {second_pair.first.name} and {second_pair.second.name}")

        dataframe = pd.DataFrame.from_dict(team_dict)
        dataframe.style.set_caption(f"Round {round_no} pairings")
        return dataframe

    @property
    def difficulty_counter(self):
        difficulty_counter = Counter()
        for match in self.matches:
            difficulty_counter[match.first.first] = match.second.score
            difficulty_counter[match.first.second] = match.second.score
            difficulty_counter[match.second.first] = match.first.score
            difficulty_counter[match.second.second] = match.first.score
        return difficulty_counter
