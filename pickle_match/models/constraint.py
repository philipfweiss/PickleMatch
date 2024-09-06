from dataclasses import dataclass
from pickle_match.models.player import Player
from pickle_match.models.pair import Pair
from typing import List

@dataclass
class Constraint:
    pair: Pair
    denied_pair: Pair
    
    def allowed(self, pair):
        match_a = pair.first == self.denied_pair.first and pair.second == self.denied_pair.second
        match_b = pair.second == self.denied_pair.first and pair.first == self.denied_pair.second
        return not (match_a or match_b)
