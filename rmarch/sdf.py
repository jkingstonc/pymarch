# SIGNED DISTANCE FUNCTIONS

import numpy as np
import math

def length(vec):
    return np.linalg.norm(vec)

def sphere_sdf(origin, pos, r):
    return math.sqrt((pos[0] - origin[0])**2 + (pos[1] - origin[1])**2 + (pos[2] - origin[2])**2) - r

def sphere_sdf_frac(origin, pos, r):
    #return math.sqrt(((origin[0] - pos[0])**2)%1 + ((origin[1] - pos[1])**2)%1 + ((origin[2] - pos[2])**2)%1) - r
    return math.sqrt(((pos[0]%1)-origin[0])**2 + ((pos[1]%1)-origin[1])**2 + ((pos[2]%1)-origin[2])**2)


def box_sdf(origin, pos, size):
    d = np.absolute(pos) - size
    return length(d)

def torus_sdf(origin, pos, t):
    q = np.array([np.linalg.norm(np.array([pos[0], pos[1]])) - t[0], pos[1]])
    return np.linalg.norm(q) - t[1]
