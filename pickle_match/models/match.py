from dataclasses import dataclass
from pickle_match.models.pair import Pair
from typing import List

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

    def to_df(self):
        ...
