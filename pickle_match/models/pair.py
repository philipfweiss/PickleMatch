from dataclasses import dataclass
from pickle_match.models.player import Player

@dataclass
class Pair:
    first: Player
    second: Player

    @property
    def average_rating(self):
        return (self.first.rating + self.second.rating) / 2
