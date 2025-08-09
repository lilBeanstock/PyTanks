from typing import TypedDict, Tuple, List

# server init parameters
HOST = "127.0.0.1"
PORT = 6969
BUFFER_SIZE = 1024

class Map(TypedDict):
    walls: List[List[Tuple[int, int]]]

MAP_DEFAULT: Map = { 
    "walls": [
        [(0,0),(50,10)], # Rectangle from (0, 0) to (50, 10)
        [(0,10),(10,10)]
    ]
}

MAPS: List[Map] = [MAP_DEFAULT]

class Direction(TypedDict):
    up: bool
    down: bool
    left: bool
    right: bool

class Turret(TypedDict):
    mouse: Tuple[int, int]
    isShooting: bool

class Player(TypedDict):
    position: Tuple[int, int]
    dimensions: Tuple[int, int]
    colour: Tuple[int, int, int]
    directions: Direction
    turret: Turret

class ServerClientPayload(TypedDict):
    map: int
    players: List[Player]
