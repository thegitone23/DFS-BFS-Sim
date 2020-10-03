import pygame
from pygame.locals import *
import time

# local imports
from drawingPrimitives import *

# global data structures

# data structure for nodes
graph = {
    
}
# to be used with traversing algorithms
visited={

}

# to be used in BFS
queue = [

]

# the DFS algorithm
def DFS(rootNode):
    if (visited[rootNode] == False) :
        visited[rootNode]=True
        TraversalDraw()
        time.sleep(1)
        for i in graph[rootNode]:
            DFS(i)

# BFS algorithm
def BFS():
    global queue
    if(len(queue) == 0):
        return 0
    node = queue.pop(0)
    for tempNode in graph[node]:
        if(not(tempNode in queue)):
            queue.append(tempNode)
    if(visited[node] == False):
        visited[node] = True
    TraversalDraw()
    time.sleep(1)
    for x in visited:
        if(visited[x] == False):            
            BFS()

# drawing logic while traversing the graph
def TraversalDraw():    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #clear the frame
    # bring up the updated screen
    for i in graph:
        if visited[i] == True:
            drawFilledCircle(i[0],i[1])
    for i in graph:
        if visited[i] == True and graph[i]:
            for endpoint in graph[i]:
                if visited[endpoint] == True:
                    drawLine(i[0],i[1],endpoint[0],endpoint[1])
    pygame.display.flip()

# main drawing logic
def draw():
    # coding logic here
    for pos in graph:
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
    print("i for insert, c for connect, d for disconnect, e for eliminate, a for DFS , b for BFS, any other key for view-only")

    connections = 0
    conNode = None
    deletions = 0
    delNode = None
    
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
                    mode = "disconnect"
                elif pygame.key.name(keyPressed) == 'e':
                    mode = "eliminate"
                elif pygame.key.name(keyPressed) == 'a':
                    mode = "DFS"
                elif pygame.key.name(keyPressed) == 'b':
                    mode = "BFS"
                else:
                    mode = "view-only"
                    print("i for insert, c for connect, d for disconnect, e for eliminate, a for DFS , b for BFS, any other key for view-only")
                print("key "+pygame.key.name(keyPressed)+" pressed, mode is "+mode)

            #mouse input handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the left button is pressed and insert mode is on
                if event.button == 1 and mode=="insert":
                    pos = pygame.mouse.get_pos()
                    flag = 0
                    if((pos[0] <= RAD or pos[0] >= WIDTH-RAD ) or (pos[1] <= RAD or pos[1] >= HEIGHT-RAD)):
                        flag = 1
                    for pos1 in graph:
                        if(flag == 1):
                            break
                        # distance with other circles
                        dist = distance(pos[0], pos[1], pos1[0], pos1[1])
                        # to check whether any circle will overlap
                        if(dist <= 2*RAD ):
                            flag = 1
                            break
                    if(flag == 0):
                        graph[pos]=[]
                        print(graph)

                # if the left button is pressed and connect mode is on
                elif event.button == 1 and mode == "connect":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            connections += 1
                            if(connections == 1):
                                conNode = node
                                print('conNode', conNode)
                                break
                            elif(connections == 2):
                                if (node != conNode) and (not (node in graph[conNode])): 
                                    print('node', node)
                                    graph[conNode].append(node)
                                    graph[node].append(conNode) 
                                connections = 0
                                break
                            

                # if the left button is pressed and disconnect mode is on
                elif event.button == 1 and mode == "disconnect":
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
                                if delNode in graph[node]:
                                    graph[delNode].remove(node)
                                    graph[node].remove(delNode)
                                deletions = 0
                                break

                # if the left button is pressed and elimenate mode is on
                elif event.button == 1 and mode == "eliminate":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            for key in graph:
                                for temp in graph[key]:
                                    if temp == node:
                                        graph[key].remove(temp)
                            del graph[node]
                            break

                # DFS TIME
                elif event.button == 1 and mode == "DFS":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            #clearing the visited list 
                            for i in graph:
                                visited[i]=False
                            DFS(node)
                            print("DFS COMPLETED, Setting mode to view-only")
                            mode="view-only"
                            break

                # BFS TIME
                elif event.button == 1 and mode == "BFS":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            #clearing the visited list 
                            for i in graph:
                                visited[i]=False
                            global queue
                            print(queue)
                            del queue[:]
                            queue.append(node)
                            BFS()
                            print("BFS COMPLETED, Setting mode to view-only")
                            mode="view-only"
                            break

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #clear the frame
        glClearColor(0.607, 0.278, 0.3, 1) # set background color
        draw() # calling the function with drawing logic
        pygame.display.flip()

# calling main()
main()
