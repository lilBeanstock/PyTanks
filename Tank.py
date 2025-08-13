# return random player configuration
from random import randint
from common import Player
from math import atan2, cos, sin

def randomPlayer() -> Player:
    width, height = 50,  50
    colour = (randint(20,255), randint(20,255), randint(0,245))
    turretColour = (colour[0]-10, colour[1]-10, colour[2]+10)
    cannonColour = (colour[0]-20, colour[1]-20, colour[2]+10)
            
    return {
        "position": (randint(0, 1280), randint(0, 720)),
        "dimensions": (width, height),
        "turret": {
            "mouse": (0,0),
            "isShooting": False,
            "dimensions": (width / 1.8, height / 5),
            "colour": turretColour,
            "cannonColour": cannonColour
        },
        "velocity": { "x": 0, "y": 0 },
        "colour": (randint(0,255), randint(0,255), randint(0,255)),
        "directions": {
            "down": False,
            "left": False,
            "right": False,
            "up": False
        },
        "kills": 0,
        "wins":0
    }

def middle(player: Player):
    return (
        player['position'][0] + player['dimensions'][0] / 2,
        player['position'][1] + player['dimensions'][1] / 2
    )

# Edge of the cannon is in the center of the tank when rotated.
def translateCannonPosition(player: Player):
    midX, midY = middle(player)
    width, _ = player['turret']['dimensions']

    # shift cannon according to mouse
    midX += (width/2)*cos(calculateMouseAngle(player)) 
    midY -= (width/2)*sin(calculateMouseAngle(player))

    return (midX, midY)

def calculateMouseAngle(player: Player):
    x, y = middle(player)
    mouseX, mouseY = player['turret']['mouse']

    return atan2(y - mouseY, mouseX - x)
