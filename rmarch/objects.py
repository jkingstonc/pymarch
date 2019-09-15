import math
import numpy as np
from transform import Transform
import sdf

class Object:
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.transform = Transform(x,y,z,rx,ry,rz)

class Sphere(Object):
    def __init__(self, rad=1, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.rad = rad
        super().__init__(x, y, z, rx, ry, rz)

    def sdf(self, pos):
        return math.sqrt((pos[0] - self.transform.pos[0])**2 + (pos[1] - self.transform.pos[1])**2 + (pos[2] - self.transform.pos[2])**2) - self.rad