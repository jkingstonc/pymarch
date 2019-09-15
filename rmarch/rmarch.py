from renderer import *
from light import *
from camera import *
from objects import *

if __name__ == "__main__":
    r = Renderer(FOV=3.14159/4)
    r.AddCamera(ProjectionCamera(x=0,y=0,z=0))
    r.AddLight(PointLight(r=0.5,g=1,b=0,x=-20,y=0,z=-5))
    r.AddObject(Sphere(rad=2,x=1,y=0,z=10))
    r.AddObject(Sphere(rad=1,x=-1,y=0,z=10))
    r.Run()
