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

    def to_df(self):
        ...

