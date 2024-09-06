import csv
from pickle_match.models.player import Player

def load_players(filename):
    players = []
    with open(filename, "r") as f:
       reader = csv.reader(f)
       for idx, (name, rating) in enumerate(reader):
           if not idx: continue
           players.append(Player(name=name, rating=float(rating)))
    
    return players
