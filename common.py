from typing import TypedDict, Tuple, List

# server init parameters
HOST = "127.0.0.1"
PORT = 6969
BUFFER_SIZE = 4096

PYGAME_WINDOW = (1280, 720)

# map default colours
FLOOR = (249, 210, 109)
WALL = (120, 100, 64)

Coordinate = Tuple[float, float]

class Map(TypedDict):
    walls: List[Tuple[Coordinate, Coordinate]]

MAP_DEFAULT: Map = { 
    "walls": [
        # Rectangle from (x1, y1) to (x2, y2)
        # Walls just outside game window
        ((-10, -10), (PYGAME_WINDOW[0], 0)), # top border
        ((PYGAME_WINDOW[0], 0), (PYGAME_WINDOW[0], PYGAME_WINDOW[1] + 10)), # right
        ((0, PYGAME_WINDOW[1]), (PYGAME_WINDOW[0], PYGAME_WINDOW[1]+10)), # bottom
        ((-10, -10), (0, PYGAME_WINDOW[1])) # left
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
    radius: int
    mouse: Coordinate
    isShooting: bool
    dimensions: Tuple[float, float]
    colour: Tuple[int, int, int]
    cannonColour: Tuple[int, int, int]

class Bullet(TypedDict):
    radius: int
    position: Coordinate
    velocity: Velocity
    colour: Tuple[int, int, int]
    bounces: int
    player_id: int

class Player(TypedDict):
    id: int
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
    timeRemaining: int # seconds
    players: List[Player]
    bullets: List[Bullet]

class ClientServerPayload(TypedDict):
    mouse: Coordinate
    directions: Direction
    isShooting: bool
