from OpenGL.GL import *
from OpenGL.GLU import *
import math

RAD = 30
WIDTH = 800
HEIGHT = 600
LEFT = 1000
RIGHT = 900

# distance between two points (x1, y1), (x2, y2)
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# defining functions for basic shapes
def drawPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def drawLine(a, b, c, d):
    glBegin(GL_LINES)
    glVertex2f(a, b)
    glVertex2f(c, d)
    glEnd()

def drawHollowCircle(x, y, r=RAD):
    lineAmount = 100  # no. of lines used to draw circle
    twoPi = math.pi * 2
    glBegin(GL_LINE_LOOP)
    for i in range(lineAmount):
        glVertex2f(
            x + (r * math.cos(i * twoPi / lineAmount)),
            y + (r * math.sin(i * twoPi / lineAmount))
        )
    glEnd()

def drawFilledCircle(x, y, r=RAD):
    triangleAmount = 30  # no. of traingles used to draw circle
    twoPi = math.pi * 2
    glBegin(GL_TRIANGLE_FAN)
    for i in range(triangleAmount):
        glVertex2f(
            x + (r * math.cos(i * twoPi / triangleAmount)),
            y + (r * math.sin(i * twoPi / triangleAmount))
        )
    glEnd()

def getDepth(x=LEFT, y=RIGHT):
    return x-y
