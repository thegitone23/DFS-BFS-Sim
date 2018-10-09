#This is a pyOpenGL+pygame project targeted to simulate DFS algorithm

#importing stuff
#pygame imports
import pygame
from pygame.locals import *
#opengl imports
from OpenGL.GL import *
from OpenGL.GLU import *
#other imports
import math
#declaring constants
RAD = 30
WIDTH = 800
HEIGHT = 600

# data structure for nodes
graph = {
    
}

# for handling positions of the nodes
position = [

]

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

# main drawing logic
def draw():
    # coding logic here
    for pos in position:
        drawHollowCircle(pos[0], pos[1])
    for node in graph:
        if(graph[node]):
            for endPoint in graph[node]:
                drawLine(node[0], node[1], endPoint[0], endPoint[1])

# main function
def main():
    # boiler-plate setup code
    pygame.init()
    display = (WIDTH, HEIGHT) # the pygame windows resolution
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluOrtho2D(0, WIDTH, HEIGHT, 0)

    # default mode
    mode="view-only" 
    print("current mode is "+mode)
    print("key-bindings are")
    print("i for insert, c for connect, d for delete, any other key for view-only")

    connections = 0
    conNode = None
    deletions = 0
    delNode = 0
    
    # the main loop
    while True:

        # event hadling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keyboard input handling
            if event.type == pygame.KEYDOWN:
                keyPressed = event.key
                if pygame.key.name(keyPressed) == 'i':
                    mode = "insert"
                elif pygame.key.name(keyPressed) == 'c':
                    mode = "connect"
                elif pygame.key.name(keyPressed) == 'd':
                    mode = "delete"
                else:
                    mode = "view-only"
                print("key "+pygame.key.name(keyPressed)+" pressed, mode is "+mode)

            #mouse input handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the left button is pressed and insert mode is on
                if event.button == 1 and mode=="insert":
                    pos = pygame.mouse.get_pos()
                    flag = 0
                    if((pos[0] <= RAD or pos[0] >= WIDTH-RAD ) or (pos[1] <= RAD or pos[1] >= HEIGHT-RAD)):
                        flag = 1
                    for pos1 in position:
                        if(flag == 1):
                            break
                        # distance with other circles
                        dist = distance(pos[0], pos[1], pos1[0], pos1[1])
                        # to check whether any circle will overlap
                        if(dist <= 2*RAD ):
                            flag = 1
                            break
                    if(flag == 0):
                        position.append(pos)
                        graph[pos]=[]
                        print(graph)
                
                # if the left button is pressed and connect mode is on
                if event.button == 1 and mode == "connect":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            connections += 1
                            if(connections == 1):
                                conNode = node
                                print('conNode', conNode)
                                break
                            elif(connections == 2):
                                print('node', node)
                                graph[conNode].append(node)
                                connections = 0
                                break

                # if the left button is pressed and delete mode is on
                if event.button == 1 and mode == "delete":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            deletions += 1
                            if(deletions == 1):
                                delNode = node
                                print('delNode', delNode)
                                break
                            elif(deletions == 2):
                                print('node', node)
                                try:
                                    graph[delNode].remove(node)
                                except:
                                    graph[node].remove(delNode)
                                deletions = 0
                                break

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #clear the frame
        draw() # calling the function with drawing logic
        pygame.display.flip() # bring up the updated screen

# calling main()
main()
