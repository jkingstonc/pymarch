import math
import numpy as np
from utils import Normalize
from transform import Transform

class Object:
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.transform = Transform(x,y,z,rx,ry,rz)

class Sphere(Object):
    def __init__(self, rad=1, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.rad = rad
        super().__init__(x, y, z, rx, ry, rz)

    def sdf(self, pos):
        return math.sqrt((pos[0] - self.transform.xyz[0])**2 + (pos[1] - self.transform.xyz[1])**2 + (pos[2] - self.transform.xyz[2])**2) - self.rad

class SphereFractal(Object):
    def __init__(self, c=1, rad=1, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.c = c
        self.rad = rad
        super().__init__(x, y, z, rx, ry, rz)

    def sdf(self, pos):
        q = np.array([(pos[0] % self.c) - 0.5*self.c,
                      (pos[1] % self.c) - 0.5*self.c,
                      (pos[2] % self.c) - 0.5*self.c])
        return math.sqrt((q[0] - self.transform.xyz[0])**2 + (q[1] - self.transform.xyz[1])**2 + (q[2] - self.transform.xyz[2])**2) - self.rad

class Box(Object):
    def __init__(self, w=1, h=1, d=1, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.dimensions = Transform(w, h, d)
        super().__init__(x, y, z, rx, ry, rz)

    def sdf(self, pos):
        return np.linalg.norm(np.array([
            max(abs(pos[0]) - self.dimensions.xyz[0], 0),
            max(abs(pos[1]) - self.dimensions.xyz[1], 0),
            max(abs(pos[2]) - self.dimensions.xyz[2], 0)
        ]), ord=1)