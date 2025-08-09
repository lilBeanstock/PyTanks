# return random player configuration
from random import randint
from common import Player
from math import atan2

def randomPlayer() -> Player:
    return {
        "position": (randint(0, 1280), randint(0, 720)),
        "dimensions": (50, 50),
        "colour": (randint(0,255), randint(0,255), randint(0,255)),
        "directions": {
            "down": False,
            "left": False,
            "right": False,
            "up": False
        },
        "turret": {
            "mouse": (0,0),
            "isShooting": False
        }
    }

def middle(player: Player):
    return (
        player['position'][0] + player['dimensions'][0] / 2,
        player['position'][1] + player['dimensions'][1] / 2
    )

def calculateAngle(player: Player):
    x, y = middle(player)
    mouseX, mouseY = player['turret']['mouse']

    return atan2(mouseY - y, mouseX - x)
