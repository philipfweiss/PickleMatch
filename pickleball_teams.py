from models.team import Team
from models.player import Player

t = Team(players=[Player("philip", 10)])

print(t.average_rating)