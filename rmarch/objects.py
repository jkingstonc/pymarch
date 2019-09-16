import math
import numpy as np
from utils import Normalize
from transform import Transform

class Object:
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.transform = Transform(x,y,z,rx,ry,rz)

class Sphere(Object):
    def __init__(self, fract=False, c=1, rad=1, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.fract = fract
        self.c = c
        self.rad = rad
        super().__init__(x, y, z, rx, ry, rz)

    def sdf(self, pos):
        if self.fract:
            return self.sdf_fract(pos)
        return math.sqrt((pos[0] - self.transform.xyz[0])**2 + (pos[1] - self.transform.xyz[1])**2 + (pos[2] - self.transform.xyz[2])**2) - self.rad

    def sdf_fract(self, pos):
        return math.sqrt(((pos[0] % self.c) - self.transform.xyz[0]) ** 2 + (
                    (pos[1] % self.c) - self.c / 2 - self.transform.xyz[1]) ** 2 + (
                                     pos[2] - self.transform.xyz[2]) ** 2) - self.rad
class SphereWobble(Sphere):
    def __init__(self, fract=False, c=1, w=5, a=1, rad=1, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.w = w
        self.a = a
        super().__init__(fract, c, rad, x, y, z, rx, ry, rz)

    def sdf(self, pos):
        return super(SphereWobble, self).sdf(pos) + (math.sin(pos[0]*self.w) * math.sin(pos[1]*self.w) * math.sin(pos[2]*self.w) * self.a)

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