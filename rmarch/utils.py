import numpy as np
import math

def MapVals(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def Normalize(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

def AngleBetween(v1, v2):
    v1_u = Normalize(v1)
    v2_u = Normalize(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

# v1 = angle of incidence, n = normal
def Reflect(v1, n):
    return v1 - 2*(np.dot(v1, n))*n