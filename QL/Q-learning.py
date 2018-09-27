#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 08:33:30 2018

@author: f

QL class made following this guide: 
    https://www.samyzaf.com/ML/rl/qmaze.html
    Themistoklis Diamantopoulos: https://github.com/thdiaman
    

2. With parameters:
    
    a) maze_in() for manual input in commandline

    b) maze_load() for getting from txts

    c) maze_n() for pre-loaded mazes 
    
"""
def maze_load():
    global start
    global size
    global end
    maze = []
    FILENAME = "maze2.txt"
    print("Loading maze from file...")
    inFile = open(FILENAME, 'r')
    size = inFile.readline().split()
    size = [ int(x1) for x1 in size ]
    print('size' + str(size))
    start = inFile.readline().split()
    start = [ int(x2) for x2 in start ]
    print('start' + str(start))
    end = inFile.readline().split()
    end = [ int(x3) for x3 in end ]
    print('end' + str(end))
    
    for x in range(size[1]):
        rw = inFile.readline().rstrip()
        rw = list(map(int, str(rw)) )
        maze.append(rw)  
    maze = invertList(maze)
    print(maze)    
    return maze

def maze_in():
    maze = []
    global start
    global size
    global end    
    size = input("insert size: ").split()
    size = [ int(x1) for x1 in size ]
    
    start = input("insert starting point: ").split()
    start = [ int(x2) for x2 in start ]
    
    end = input("insert ending point: ").split()
    end = [ int(x3) for x3 in end ]

    for x in range(size[1]):
        rw = input("insert row #" + str(x+1) + ": ")
        rw = list(map(int, str(rw)) )
        maze.append(rw)        
    maze [((len(maze) - 1) - end[1])] [end[0]] = 2
    maze = invertList(maze)
    print(maze)
    return maze  


def visualize(maze):
    global start
    global end
    startx = int(start[0])
    starty = int(start[1])
    endx = int(end[0])
    endy = int(end[1])
    maze [starty] [startx] = 'S' 
    maze [endy] [endx] = 'E' 
    maze = [['▓' if x==1 else x for x in row] for row in maze]
    maze = [['e' if x==2 else x for x in row] for row in maze]
    maze = [['░' if x==0 else x for x in row] for row in maze]
    maze = [['.' if x==3 else x for x in row] for row in maze]
    maze = [['X' if x==4 else x for x in row] for row in maze]
    maze = invertList(maze)
    print('\n'.join(''.join(row) for row in maze))  
    print("____________________")    
    
    
def invertList(listToInvert):
    newList = []
    listLen = len(listToInvert)
    for index in range(listLen):
        newList.append(listToInvert[listLen - index - 1])
    return newList

def findwalls(maze):
    walls = []
    for idx_y, row in enumerate(maze):
        for idx_x, cell in enumerate(row):
            if cell == 1:
                walls.insert(0,(idx_x,idx_y))
    #vizwalls(walls, maze)
    return walls
    

def traildir(trail, maze):
    for element in trail:
        try:
            maze [element[1]][element[0]] = 3
        except IndexError:
            print("indexerror" + str(element))
            return False
    visualize(maze)    
        
def main(maze):
    global start
    global end
    global size
    start = tuple(start)
    end = tuple(end)
    width = int(size[0])
    height = int(size[1])
    print(path) 

def main_visual(maze):
    global start
    global end
    global size
    start = tuple(start)
    end = tuple(end)
    width = int(size[0])
    height = int(size[1])
    print("unsolved:")
    visualize(maze)
    path, trail = a.solve()
    print("solved: ")
    traildir(trail, maze)
    print('path: ' + path) 
    #print(trail)
    
main(maze_3())
