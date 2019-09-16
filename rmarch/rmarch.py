from renderer import *
from light import *
from camera import *
from objects import *
from sdf import SDF

if __name__ == "__main__":
    r = Renderer(WIDTH=1000, HEIGHT=700, FOV=3.14159/2, SDF_TYPE=SDF.SMOOTH_MIN)
    r.AddCamera(ProjectionCamera(x=0,y=0,z=0))
    r.AddLight(PointLight(r=1,g=1,b=0,x=-15,y=15,z=-1))
    r.AddLight(PointLight(r=0, g=1, b=0, x=5, y=-5, z=-15))
    r.AddObject(SphereWobble(fract=True, c=5, w=5, a=2, rad=1, x=3, y=0, z=15))
    r.Run()
