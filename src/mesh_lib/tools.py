DEFAULT_VERTEX_COUNT = 10
import math
from .vec3 import Vec3

def vertCircle(builder=None, centre=Vec3((0,0,0)), radius=1, vertexCount=DEFAULT_VERTEX_COUNT, group=None):
    for i in range(vertexCount):
        theta = i*2*math.pi/vertexCount
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        z = 0
        builder.vertices.addVertex(centre.add((x,y,z)), group)

def vertSpiral(builder=None, centre=Vec3((0,0,0)), radius=1, height=1, vertexCount=DEFAULT_VERTEX_COUNT, group=None):
    heightIncrement = height/vertexCount
    angleIncrement = 2*math.pi/vertexCount
    for i in range(vertexCount):
        theta = i*angleIncrement
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        z = i*heightIncrement
        builder.vertices.addVertex(centre.add((x,y,z)), group)