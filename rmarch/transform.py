import numpy as np

class Transform:
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0):
        self.xyz = np.array([x,y,z])
        self.rot = np.array([rx,ry,rz])

    def Translate(self, x=0, y=0, z=0):
        self.xyz[0]+=x
        self.xyz[1]+=y
        self.xyz[2]+=z

    def SetPos(self, x=0, y=0, z=0):
        self.xyz[0]=x
        self.xyz[1]=y
        self.xyz[2]=z

    def Rotate(self, rx=0, ry=0, rz=0):
        self.rot[0]+=rx
        self.rot[1]+=ry
        self.rot[2]+=rz

    def SetRot(self, rx=0, ry=0, rz=0):
        self.rot[0]=rx
        self.rot[1]=ry
        self.rot[2]=rz