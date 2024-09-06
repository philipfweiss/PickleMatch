import csv
from pickle_match.models.player import Player

def load_players(filename=None, players=None):
    player_objects = []

    if filename:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for idx, (name, rating) in enumerate(reader):
                if not idx: continue
                players.append(Player(name=name, rating=float(rating)))
    elif csv:
        for (name, rating) in players:
            player_objects.append(Player(name=name, rating=float(rating)))

    return player_objects
