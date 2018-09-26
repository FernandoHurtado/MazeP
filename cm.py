import heapq


class Cell(object):
    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


class AStar(object):
    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = None
        self.grid_width = None

    def init_grid(self, width, height, walls, start, end):

        self.grid_height = height
        self.grid_width = width
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):

        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def solve(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, return found path
            if cell is self.end:
                return self.get_path()
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


#!/usr/bin/env python3



# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 19:39:23 2018

@author: f
"""
grid = []
def create_maze():
    maze = []
    global start
    size = input("insert size: ").split()
    size = [ int(x1) for x1 in size ]
    
    start = input("insert starting point: ").split()
    start = [ int(x2) for x2 in start ]
    
    end = input("insert starting point: ").split()
    end = [ int(x3) for x3 in end ]

    for x in range(size[1]):
        rw = input("insert row #" + str(x+1) + ": ")
        #might want to add a point here later on
        rw = list(map(int, str(rw)) )
        maze.append(rw)        
    maze [((len(maze) - 1) - end[1])] [end[0]] = "2"
    maze = invertList(maze)
    print(maze)
    return maze  


def visualize(maze):
    print("____________________")
    maze = [['#' if x==1 else x for x in row] for row in maze]
    maze = [[' ' if x==0 else x for x in row] for row in maze]
    maze = [['E' if x==2 else x for x in row] for row in maze]
    maze = [['.' if x==3 else x for x in row] for row in maze]
    maze = invertList(maze)
    print('\n'.join(''.join(row) for row in maze)) 
    
    
def invertList(listToInvert):
    newList = []
    listLen = len(listToInvert)
    for index in range(listLen):
        newList.append(listToInvert[listLen - index - 1])
    return newList

def test_maze_1():
    global start
    global size
    global end
    size = [15,11]
    start = [0,0]
    end = [12,2]
    return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, '2', 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]]

def test_maze_2():
    global start
    global size
    global end
    size = [6,6]
    start = [0,0]
    end = [6,6]
    return[[0, 0, 0, 0, 0, 1],[1, 1, 0, 0, 0, 1],[0, 0, 0, 1, 0, 0],[0, 1, 1, 0, 0, 1],[0, 1, 0, 0, 1, 0],[0, 1, 0, 0, 0, 2]]


def recursivesearch(x, y):
    visualize(grid)
    if grid[x][y] == 2:
        print ('found at %d,%d' % (x, y))
        return True
    elif grid[x][y] == 1:
        print ('wall at %d,%d' % (x, y))
        return False
    elif grid[x][y] == 3:
        print ('visited at %d,%d' % (x, y))
        return False
    
    print ('visiting %d,%d' % (x, y))

    # mark as visited
    grid[x][y] = 3

    # explore neighbors clockwise starting by the one on the right
    if ((x < len(grid)-1 and recursivesearch(x+1, y))
        or (y > 0 and recursivesearch(x, y-1))
        or (x > 0 and recursivesearch(x-1, y))
        or (y < len(grid)-1 and recursivesearch(x, y+1))):
        return True

    return False

def findwalls(maze):
    global size
    walls = ()
    x= 0
    y= 0
    while y < size[0] - 1:
        y += 1
        while x < size[1] - 1:
            x += 1
            if maze[y][x] == 1:
                walls = ((x,y),) + walls
    return walls

def pathdir(path, maze):
    for element in path:
        try:
            maze [element[1]][element[0]] = 3
        except IndexError:
            print("indexerror" + str(element))
            return False
    visualize(maze)    
        

def main():
    maze = test_maze_1()
    #############
    global start
    global end
    global size
    start = tuple(start)
    end = tuple(end)
    width = int(size[0])
    height = int(size[1])
    a = AStar()
    walls = findwalls(maze)
    visualize(maze)
    a.init_grid(width, height, walls, start, end)
    path = a.solve()
    pathdir(path, maze)
    print(path)
    
main()
