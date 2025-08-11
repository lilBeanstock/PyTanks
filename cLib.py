import ctypes
from os import path
from common import Map
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
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]

class DirectionC(ctypes.Structure):
    _fields_ = [("up", ctypes.c_bool),
                ("down", ctypes.c_bool),
                ("left", ctypes.c_bool),
                ("right", ctypes.c_bool)]

class PlayerC(ctypes.Structure):
    _fields_ = [("position", PointC),
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

# define types
lib.rectangles_overlap.argtypes = (RectangleC, RectangleC)  # Specify argument types
lib.rectangles_overlap.restype = ctypes.c_bool            # Specify return type

def translateMapC(map: Map):
    walls = map["walls"]
    wallcount = len(map["walls"])

    cWalls: List[WallC] = []

    for wall in walls:
        wStart = PointC(wall[0][0],wall[0][1])
        wEnd = PointC(wall[1][0],wall[1][1])

        structWall = WallC(wStart,wEnd)
        cWalls.append(structWall)

    # make cWalls into a pointer and return the pointer
    pcWalls = (WallC * wallcount)(*cWalls) # create an initialiser class in the first bracket, then initialise it with *cWalls

    c_Map: MapC = MapC(pcWalls ,wallcount)
    return c_Map
