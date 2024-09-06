from dataclasses import dataclass
from pickle_match.models.player import Player

@dataclass(frozen=True)
class Pair:
    first: score + self.second.score
    second: Player
    team_id: int

    @property
    def average_rating(self):
        return (self.first.rating + self.second.rating) / 2

    @property
    def score(self):
        return self.first.score + self.second.score
