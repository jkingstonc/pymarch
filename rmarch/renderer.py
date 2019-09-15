import sys
import pygame
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
import math

from utils import MapVals, Normalize, AngleBetween, Reflect

class Renderer:
    def __init__(self, WIDTH=1280, HEIGHT=720, FOV=3.14159/2, USE_GPU=False):
        self.frame = 0
        self.FPS = 30
        self.WIDTH=WIDTH
        self.HEIGHT=HEIGHT
        self.ASP = WIDTH/HEIGHT
        self.current_pix_density = 64
        self.FOV=FOV
        self.MARCH_STEPS = 1000 # Max march steps, the higher the more detail
        self.EPSILON = 0.1 # Tollerance of ray hit, the smaller, the more detail
        self.END = 5000 # Max marching distance
        self.camera = None
        self.lights = []
        self.scene_objects = []

        self.USE_GPU = USE_GPU
        self.x_pixels = np.array([], dtype=np.int32)
        self.y_pixels = np.array([], dtype=np.int32)
        # setup the pixel arrays for CUDA parrallelizations
        if USE_GPU:
            for i in range(0, self.WIDTH):
                for j in range(0, self.HEIGHT):
                    np.append(self.x_pixels, i)
                    np.append(self.y_pixels, j)

    def AddCamera(self, camera):
        self.camera = camera

    def AddLight(self, light):
        self.lights.append(light)

    def AddObject(self, obj):
        self.scene_objects.append(obj)

    def Update(self, dt):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.set_caption("FPS: "+str(dt))
        
    def Draw(self, screen):
        screen.fill((0, 0, 0))
        for x in range(0, self.WIDTH):
            if x % self.current_pix_density == 0:
                for y in range(0, self.HEIGHT):
                    if y % self.current_pix_density == 0:
                        self.CalculateRay(screen, x, y)
        if self.current_pix_density  != 1:
            self.current_pix_density/=2
        pygame.display.flip()
    
    def Run(self):
        pygame.init()
        fpsClock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        dt = 1/self.FPS
        while True:
            self.Update(dt)
            self.Draw(screen)
            dt = fpsClock.tick(self.FPS)
            self.frame+=1

    def CalculateRay(self, screen, x, y):
        # https://learnopengl.com/Lighting/Basic-Lighting for shading
        steps = 0
        depth = 0
        x_angle = MapVals(x, 0, self.WIDTH, -self.FOV/2, self.FOV/2)*self.ASP # the x angle of this ray 
        y_angle = MapVals(y, 0, self.HEIGHT, -self.FOV/2, self.FOV/2) # the y angle of this ray 
        direction = np.array([math.sin(x_angle), math.sin(y_angle), 1]) # turning these angles into a vector
        for i in range(0, self.MARCH_STEPS):
            point = (self.camera.transform.pos + depth) * direction
            dist = self.SceneSDF(point)
            if dist < self.EPSILON:
                # INSIDE SURFACE
                norm = self.SurfaceNormalEstimate(point)

                ambiend_rgb = [0.1,0.1,0.1]
                diff_rgb = [1,1,1]
                spec_rgb = [1,1,1]
                sum_rgb = [0,0,0]
                for light in self.lights:
                    light_dir = Normalize(light.transform.pos - point)
                    # Calculate diffuse intensity
                    diff_intensity = np.dot(light_dir, norm)
                    diff_rgb[0] *= (diff_intensity * light.colour[0])
                    diff_rgb[1] *= (diff_intensity * light.colour[1])
                    diff_rgb[2] *= (diff_intensity * light.colour[2])
                    # Calculate specular intensity
                    spec_power = 8
                    spec_strength = 0.5
                    reflect_dir = Reflect(light_dir, norm)
                    spec = math.pow(np.dot(light_dir, reflect_dir), spec_power)
                    spec_intensity = spec_strength * spec
                    spec_rgb[0] *= (spec_intensity * light.colour[0])
                    spec_rgb[1] *= (spec_intensity * light.colour[1])
                    spec_rgb[2] *= (spec_intensity * light.colour[2])
                sum_rgb[0]=ambiend_rgb[0]+diff_rgb[0]+spec_rgb[0]
                sum_rgb[1]=ambiend_rgb[1]+diff_rgb[1]+spec_rgb[1]
                sum_rgb[2]=ambiend_rgb[2]+diff_rgb[2]+spec_rgb[2]
                sum_rgb[0]=int(MapVals(sum_rgb[0], -1, 1, 0, 255))
                sum_rgb[1]=int(MapVals(sum_rgb[1], -1, 1, 0, 255))
                sum_rgb[2]=int(MapVals(sum_rgb[2], -1, 1, 0, 255))
                gfxdraw.pixel(screen, x, y, (sum_rgb[0],sum_rgb[1],sum_rgb[2]))
                break
            depth += dist
            steps += 1
            if depth >= self.END:
                # GONE TOO FAR
                break

    def SceneSDF(self, pos):
        #return sdf.sphere_sdf(np.array([0,0,5]), pos, 1)
        min_val = self.END
        for obj in self.scene_objects:
            val = obj.sdf(pos)
            if val < min_val:
                min_val = val
        return min_val

    def SurfaceNormalEstimate(self, pos):
        return Normalize(np.array([
            self.SceneSDF(np.array([pos[0] + self.EPSILON, pos[1], pos[2]])) - self.SceneSDF(np.array([pos[0] - self.EPSILON, pos[1], pos[2]])),
            self.SceneSDF(np.array([pos[0], pos[1] + self.EPSILON, pos[2]])) - self.SceneSDF(np.array([pos[0], pos[1] - self.EPSILON, pos[2]])),
            self.SceneSDF(np.array([pos[0], pos[1], pos[2]  + self.EPSILON])) - self.SceneSDF(np.array([pos[0], pos[1], pos[2] - self.EPSILON]))
        ]))
