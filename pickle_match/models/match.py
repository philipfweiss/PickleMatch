from dataclasses import dataclass
from pickle_match.models.pair import Pair

@dataclass
class Match:
    first: Pair
    second: Pair
