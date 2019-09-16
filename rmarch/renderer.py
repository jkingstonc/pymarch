import sys
import pygame
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
import math
import random
from sdf import *

from utils import MapVals, Normalize, AngleBetween, Reflect

class Renderer:
    def __init__(self, WIDTH=600, HEIGHT=400, FOV=3.14159/2, SDF_TYPE=SDF.MIN):
        self.frame = 0
        self.FPS = 30
        self.WIDTH=WIDTH
        self.HEIGHT=HEIGHT
        self.ASP = WIDTH/HEIGHT
        self.CYCLES = 100
        self.WIDTH_BLOCKS = int(self.WIDTH/self.CYCLES)
        self.HEIGHT_BLOCKS = int(self.HEIGHT/self.CYCLES)
        self.FOV=FOV
        self.MARCH_STEPS = 1000 # Max march steps, the higher the more detail
        self.EPSILON = 0.1 # Tollerance of ray hit, the smaller, the more detail
        self.END = 5000 # Max marching distance
        self.BACKGROUND_COLOUR = (0,0,100)
        self.GLOW_THRESHOLD = self.END
        self.camera = None
        self.lights = []
        self.scene_objects = []
        self.SDF_TYPE = SDF.MIN

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
        for x in range(0, self.CYCLES):
            for y in range(0, self.CYCLES):
                x_pixel = x*self.WIDTH_BLOCKS + random.randint(0,self.WIDTH_BLOCKS)
                y_pixel = y*self.HEIGHT_BLOCKS + random.randint(0,self.HEIGHT_BLOCKS)
                gfxdraw.pixel(screen, x_pixel, y_pixel, self.CalculateRay(screen, x_pixel, y_pixel))
        pygame.display.flip()
    
    def Run(self):
        pygame.init()
        fpsClock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        dt = 1/self.FPS
        for i in range(self.CYCLES):
            self.Update(dt)
            self.Draw(screen)
            dt = fpsClock.tick(self.FPS)
            self.frame+=1
        while True:
            pass

    def CalculateRay(self, screen, x, y):
        # https://learnopengl.com/Lighting/Basic-Lighting for shading
        steps = 0
        depth = 0
        max_steps = 1
        x_angle = MapVals(x, 0, self.WIDTH, -self.FOV/2, self.FOV/2)*self.ASP # the x angle of this ray 
        y_angle = MapVals(y, 0, self.HEIGHT, -self.FOV/2, self.FOV/2) # the y angle of this ray 
        direction = np.array([math.sin(x_angle), math.sin(y_angle), 1]) # turning these angles into a vector
        for i in range(0, self.MARCH_STEPS):
            point = (self.camera.transform.xyz + depth) * direction
            dist = self.SceneSDF(point)
            if dist < self.EPSILON:
                # INSIDE SURFACE
                norm = self.SurfaceNormalEstimate(point)

                ambiend_rgb = [0.1,0.1,0.1]
                diff_rgb = [0,0,0]
                spec_rgb = [0,0,0]
                sum_rgb = [0,0,0]
                light_level = len(self.lights)
                if(len(self.lights)==0):
                    light_level=1
                for light in self.lights:
                    light_dir = Normalize(light.transform.xyz - point)
                    # Calculate diffuse intensity
                    diff_intensity = np.dot(light_dir, norm)
                    # Calculate specular intensity
                    spec_power = 32
                    spec_strength = 1
                    reflect_dir = Reflect(light_dir, norm)
                    spec = math.pow(np.dot(light_dir, reflect_dir), spec_power)
                    spec_intensity = spec_strength * spec
                    for i in range(0, 3):
                        diff_rgb[i] += (diff_intensity * light.colour[i])
                        spec_rgb[i] += (spec_intensity * light.colour[i])
                for i in range(0, 3):
                    sum = ambiend_rgb[i]+diff_rgb[i]+spec_rgb[i]
                    if sum < 0:
                        sum = 0
                    #sum_rgb[i]=int(MapVals(sum, 0, light_level, 0, 255))
                    sum_rgb[i] = int(MapVals(sum, 0, 1, 0, 255))
                    if sum_rgb[i] > 255:
                        sum_rgb[i]=255
                return (sum_rgb[0], sum_rgb[1], sum_rgb[2])
            depth += dist
            steps += 1
            if depth >= self.END:
                if steps > max_steps:
                    max_steps = steps
                # Gone too far
                # Apply edge glow
                if steps >= self.GLOW_THRESHOLD:
                    col = MapVals(steps, self.GLOW_THRESHOLD, max_steps+1, self.BACKGROUND_COLOUR[0], 255)
                    return (col,col,col)
                return self.BACKGROUND_COLOUR

    def SceneSDF(self, pos):
        operator = None
        start_val = 0
        if self.SDF_TYPE == SDF.SMOOTH_MIN:
            start_val = self.END
            for obj in self.scene_objects:
                val = obj.sdf(pos)
                start_val = self.SmoothMin(start_val, val, 1)
            return start_val
        elif self.SDF_TYPE == SDF.SMOOTH_MAX:
            start_val = 0
            for obj in self.scene_objects:
                val = obj.sdf(pos)
                start_val = self.SmoothMax(start_val, val, 1)
            return start_val
        elif self.SDF_TYPE == SDF.MIN:
            start_val = self.END
            operator = lambda a, b : a < b
        elif self.SDF_TYPE == SDF.MAX:
            start_val = 0
            operator = lambda a, b : a > b
        for obj in self.scene_objects:
            val = obj.sdf(pos)
            if operator(val, start_val):
                start_val = val
        return start_val

    def SurfaceNormalEstimate(self, pos):
        return Normalize(np.array([
            self.SceneSDF(np.array([pos[0] + self.EPSILON, pos[1], pos[2]])) - self.SceneSDF(np.array([pos[0] - self.EPSILON, pos[1], pos[2]])),
            self.SceneSDF(np.array([pos[0], pos[1] + self.EPSILON, pos[2]])) - self.SceneSDF(np.array([pos[0], pos[1] - self.EPSILON, pos[2]])),
            self.SceneSDF(np.array([pos[0], pos[1], pos[2]  + self.EPSILON])) - self.SceneSDF(np.array([pos[0], pos[1], pos[2] - self.EPSILON]))
        ]))

    def SmoothMin(self, a, b, k):
        h = 0.5 + 0.5 * (b-a)/k
        if h > 1:
            h=1
        elif h < 0:
            h=0
        # b a h
        return (b * (1 - h) + a * h) - k*h*(1-h)

    def SmoothMax(self, a, b, k):
        h = 0.5 - 0.5 * (b-a)/k
        if h > 1:
            h=1
        elif h < 0:
            h=0
        # b a h
        return (b * (1 - h) + a * h) - k*h*(1-h)
