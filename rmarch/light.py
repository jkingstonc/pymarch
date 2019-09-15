from transform import Transform

class Light:
    def __init__(self, r, g, b):
        self.colour = (r, g, b)

class PointLight(Light):
    def __init__(self, r=255, g=255, b=255, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.transform = Transform(x,y,z,rx,ry,rz)
        super().__init__(r,g,b)