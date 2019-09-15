from transform import Transform

class Camera:
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.transform = Transform(x,y,z,rx,ry,rz)

class OrthographicCamera(Camera):
    pass

class ProjectionCamera(Camera):
    pass