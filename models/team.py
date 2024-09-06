from dataclasses import dataclass
from models.player import Player
from typing import List

@dataclass
class Team:
    NUM_PLAYERS = 4
    players: List[Player]

    @property
    def average_rating(self):
        return sum(player.score for player in self.players) / self.NUM_PLAYERS
