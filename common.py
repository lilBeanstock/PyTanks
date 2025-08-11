from typing import TypedDict, Tuple, List

# server init parameters
HOST = "127.0.0.1"
PORT = 6969
BUFFER_SIZE = 4096

# map default colours
FLOOR = (249, 210, 109)
WALL = (120, 100, 64)

Coordinate = Tuple[int, int]

class Map(TypedDict):
    walls: List[Tuple[Coordinate, Coordinate]]

MAP_DEFAULT: Map = { 
    "walls": [
        ((0,0),(100,10)), # Rectangle from (0, 0) to (50, 10)
        ((0,50),(100,60))
    ]
}

MAPS: List[Map] = [MAP_DEFAULT]

class Velocity(TypedDict):
    x: float
    y: float

class Direction(TypedDict):
    up: bool
    down: bool
    left: bool
    right: bool

class Turret(TypedDict):
    mouse: Coordinate
    isShooting: bool
    dimensions: Tuple[float, float]
    colour: Tuple[int, int, int]
    cannonColour: Tuple[int, int, int]

class Player(TypedDict):
    position: Coordinate
    dimensions: Tuple[int, int]
    colour: Tuple[int, int, int]
    directions: Direction
    velocity: Velocity
    turret: Turret
    kills: int # kills in each match, resets with new
    wins: int

class ServerClientPayload(TypedDict):
    map: int
    players: List[Player]
    timeRemaining: int # seconds

class ClientServerPayload(TypedDict):
    mouse: Coordinate
    directions: Direction
    isShooting: bool
