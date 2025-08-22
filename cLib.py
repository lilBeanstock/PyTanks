import ctypes
from os import path
from common import Player, Map, Direction, Velocity, Bullet
from typing import List

# Load the shared library
lib = ctypes.CDLL(path.join(path.dirname(__file__), "lib.so"))

# Define the Rectangle structure in Python
class RectangleC(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int),
                ("width", ctypes.c_int),
                ("height", ctypes.c_int)]

class VelocityC(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]

class PointC(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]

class DirectionC(ctypes.Structure):
    _fields_ = [("up", ctypes.c_bool),
                ("down", ctypes.c_bool),
                ("left", ctypes.c_bool),
                ("right", ctypes.c_bool)]

class PlayerC(ctypes.Structure):
    _fields_ = [("id", ctypes.c_int),
                ("position", PointC),
                ("dimensions", PointC),
                ("colour", ctypes.c_ubyte * 3),
                ("directions", DirectionC),
                ("velocity", VelocityC),
                ("kills", ctypes.c_int),
                ("wins", ctypes.c_int)]

class WallC(ctypes.Structure):
    _fields_ = [("start", PointC),
                ("end", PointC)]

class MapC(ctypes.Structure):
    _fields_ = [("walls", ctypes.POINTER(WallC)),
                ("wall_count", ctypes.c_int)]

class BulletC(ctypes.Structure):
    _fields_ = [
         ("radius", ctypes.c_int),
         ("position", PointC),
         ("velocity", VelocityC),
         ("colour", ctypes.c_ubyte*3),
         ("bounces", ctypes.c_int),
         ("player_id", ctypes.c_int)
    ]

# define types
lib.rectangles_overlap.argtypes = (RectangleC, RectangleC)  # Specify argument types
lib.rectangles_overlap.restype = ctypes.c_bool            # Specify return type

lib.handle_all.argtypes = (MapC, ctypes.POINTER(PlayerC), ctypes.c_size_t, ctypes.POINTER(BulletC), ctypes.c_size_t)  # Specify argument types
lib.handle_all.restype = None           # Specify return type

def translateMapC(map: Map):
    walls = map["walls"]
    wallcount = len(walls)

    cWalls: List[WallC] = []

    for wall in walls:
        wStart = PointC(wall[0][0],wall[0][1])
        wEnd = PointC(wall[1][0],wall[1][1])

        structWall = WallC(wStart,wEnd)
        cWalls.append(structWall)

    # make cWalls into a pointer and return the pointer
    pcWalls = (WallC * wallcount)(*cWalls) # create an initialiser class in the first bracket, then initialise it with *cWalls

		# build MapC and attach the buffer to it so Python keeps it alive
    c_Map = MapC()
    c_Map.walls = ctypes.cast(pcWalls, ctypes.POINTER(WallC))
    c_Map.wall_count = wallcount
    # attach the buffer to the MapC instance (prevents GC)
    c_Map._walls_buf = pcWalls

    return c_Map

def translatePlayerC(player: Player) -> PlayerC:
    c_id = ctypes.c_int(player["id"])
    c_pos = PointC(player["position"][0],player["position"][1])
    c_dim = PointC(player["dimensions"][0],player["dimensions"][1])
    c_col = (ctypes.c_ubyte * 3)(
        player["colour"][0],
        player["colour"][1],
        player["colour"][2]
    )
    c_dir = DirectionC(
        player["directions"]["up"],
        player["directions"]["down"],
        player["directions"]["left"],
        player["directions"]["right"]
    )
    c_vel = VelocityC(player["velocity"]["x"],player["velocity"]["y"])
    c_kill = ctypes.c_int(player["kills"])
    c_win = ctypes.c_int(player["wins"])

    c_player = PlayerC(c_id, c_pos,c_dim,c_col,c_dir,c_vel,c_kill,c_win)
    return c_player

def makePlayerArr(playerList: List[Player]):
    convertedPlayers = [translatePlayerC(p) for p in playerList]
    players_arr = (PlayerC * len(convertedPlayers))(*convertedPlayers)
    # keep it alive by returning the array object (the caller should keep it)
    return players_arr

def translatePlayerPython(c_player: PlayerC) -> Player:
    pId = c_player.id
    pos = (c_player.position.x, c_player.position.y)
    dim = (c_player.dimensions.x, c_player.dimensions.y)
    col = (
        c_player.colour[0],
        c_player.colour[1],
        c_player.colour[2]
    )
    dir: Direction = {
        "up": c_player.directions.up,
        "down": c_player.directions.down,
        "left": c_player.directions.left,
        "right": c_player.directions.right,
    }
    vel: Velocity = {
        "x": c_player.velocity.x, 
        "y": c_player.velocity.y
    }
    kill = c_player.kills
    win = c_player.wins

    player: Player = {
        "id": pId,
        "position": pos,
        "dimensions": dim,
        "colour": col,
        "directions": dir,
        "velocity": vel,
        "kills": kill,
        "wins": win,
        "turret": {
            "radius": 0,
            "mouse": (0,0),
            "isShooting": False,
            "dimensions": (0, 0),
            "colour": (0,0,0),
            "cannonColour": (0,0,0)
        }
    }
    return player

def makePlayerList(cPlayerList: ctypes.Array[PlayerC],pyPlayerList: List[Player]):
    convertedPlayers: List[Player] = []

    if len(pyPlayerList) == 0: return pyPlayerList

    for i in range(len(pyPlayerList)):
        convertedPlayers.append(translatePlayerPython(cPlayerList[i]))
        convertedPlayers[len(convertedPlayers)-1]["turret"] = pyPlayerList[i]["turret"] 
        # reset turret info, because it is not used or transmitted by the C counterparts

    return convertedPlayers

def translateBulletC(bull: Bullet):
    c_id = ctypes.c_int(bull["player_id"])
    c_pos = PointC(bull["position"][0],bull["position"][1])
    c_vel = VelocityC(bull["velocity"]["x"],bull["velocity"]["y"])
    c_col = (ctypes.c_ubyte * 3)(
        bull["colour"][0],
        bull["colour"][1],
        bull["colour"][2]
    )
    c_rad = ctypes.c_int(bull["radius"])
    c_bou = ctypes.c_int(bull["bounces"])

    return BulletC(c_rad,c_pos,c_vel,c_col,c_bou,c_id)

def makeBulletArr(bulletList: List[Bullet]):
    cBulletList = [translateBulletC(b) for b in bulletList]
    bullets_arr = (BulletC * len(bulletList))(*cBulletList)
    return bullets_arr

def translateBulletPython(bull: BulletC):
    id = bull.player_id
    pos = (bull.position.x, bull.position.y)
    vel: Velocity = {
        "x": bull.velocity.x, 
        "y": bull.velocity.y
    }
    col = (
        bull.colour[0],
        bull.colour[1],
        bull.colour[2]
    )
    rad = bull.radius
    bou = bull.bounces

    bulletpy: Bullet = {
        "player_id": id,
        "velocity": vel,
        "colour": col,
        "radius": rad,
        "position": pos,
        "bounces": bou
    }
    return bulletpy

def makeBulletList(BulletList: ctypes.Array[BulletC]):
    pybulletList: List[Bullet] = []

    for i in BulletList:
        pybulletList.append(translateBulletPython(i))

    return pybulletList