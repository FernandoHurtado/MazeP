#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is much slower than the other version, not sure why
@author: f
"""

import heapq
import time



start_time = time.time()

def visualize(maze):
    global start
    global end
    startx = int(start[0])
    starty = int(start[1])
    endx = int(end[0])
    endy = int(end[1])
    maze [starty] [startx] = 'S' 
    maze [endy] [endx] = 'E' 
    maze = [['░' if x==0 else x for x in row] for row in maze]
    maze = [[' ' if x==2 else x for x in row] for row in maze]
    maze = [['.' if x==3 else x for x in row] for row in maze]
    maze = [['█' if x==1 else x for x in row] for row in maze]
    maze = [['X' if x==4 else x for x in row] for row in maze]
    maze.reverse()
    print('\n'.join(''.join(row) for row in maze))  
    print("____________________")    
    
def maze_load():
    global start_time
    global start
    global size
    global end

    maze = []
    FILENAME = "maze6.txt"
    inFile = open(FILENAME, 'r')
    size = inFile.readline().split()
    size = [ int(x1) for x1 in size ]
    start = inFile.readline().split()
    start = [ int(x2) for x2 in start ]
    end = inFile.readline().split()
    end = [ int(x3) for x3 in end ]  
    for x in range(size[1]):
        rw = inFile.readline().rstrip()
        
        rw = list(map(int, str(rw)) )
        maze.append(rw)  
    maze.reverse()
    return maze

def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


def astar(start, goal, Map):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    #closest_match = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:

        current = heapq.heappop(oheap)[1]
    
        if current == goal:
            length = 0
            data = []
            path = ''
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.reverse()
            for element in data:
                if length == 0:
                    prevx = element[0]
                    prevy = element[1]
                if element[0] > prevx:
                    path += 'R'
                if element[1] > prevy:
                    path += 'U'
                if element[0] < prevx:
                    path += 'L'
                if element[1] < prevy:
                    path += 'D'
                length += 1    
                prevx = element[0]
                prevy = element[1]
            return path

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < MAP_WIDTH: 
                if 0 <= neighbor[1] < MAP_HEIGHT: 
                    if Map[neighbor[1]] [neighbor[0]] == 1:  
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                #closest_match = [current]
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current

                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False
        
def traildir(trail, maze):
    for element in trail:
        try:
            maze [element[1]][element[0]] = 3
        except IndexError:
            print("indexerror" + str(element))
            return False
    visualize(maze)    
    
def main(maze): 
    global MAP_WIDTH
    global MAP_HEIGHT
    global start
    global end
    global size
    start = tuple(start)
    end = tuple(end)
    MAP_WIDTH = int(size[0])
    MAP_HEIGHT = int(size[1])
    visualize(maze)
    path = astar(start, end, maze)
    traildir(path, maze)
    print(path) 

    
main(maze_load())
print("maze of size: " + str(size) + "completed in:")
print("--- %s seconds ---" % (time.time() - start_time))