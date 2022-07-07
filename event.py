import json

def movement_event(player, x, y):
    return json.dumps({"type": "MOVEMENT", "player": player, "x": x, "y": y})

def winner_event(player):
    return json.dumps({"type": "WINNER", "player": player })
