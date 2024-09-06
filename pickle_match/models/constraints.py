from dataclasses import dataclass
from pickle_match.models.player import Player
from pickle_match.models.pair import Pair
from typing import List

@dataclass(frozen=True)
class Constraints:
    pair: Pair
    constraints: List[Pair]

    def add(self, pair):
        self.constraints.append(pair)
    
    def allowed(self, pair):
        for constraint in self.constraints:
            match_a = constraint.first == pair.first and constraint.second == pair.second
            match_b = constraint.first == pair.second and constraint.second == pair.first
            if match_a or match_b:
                return False
        return True
