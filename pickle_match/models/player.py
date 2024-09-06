from dataclasses import dataclass

@dataclass(frozen=True)
class Player:
    name: str
    rating: float
    score: int = 0
    team_id: int = -1
