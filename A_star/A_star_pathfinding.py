import heapq

"""
Created on Tue Sep 25 19:39:23 2018

@author: F

maze workshop attempt n.3: A star search

A* class made following this guide: 
    https://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
    Laurent Luce: https://github.com/laurentluce
    
    
-----
How to use:
1. Call:
    
    a)  main_visual() to show pretty maze pictures
    
    b)  main() to only output path in Left,Right,Up,Down   

2. With parameters:
    
    a) maze_in() for manual input in commandline

    b) maze_load() for getting from txts

    c) maze_n() for pre-loaded mazes 
    
"""
def maze_load(): # load from textfile
    global start
    global size
    global end
    maze = []
    FILENAME = "maze7.txt"
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
    maze.reverse()
    print('\n'.join(''.join(row) for row in maze))  
    print("____________________")    
    

class Node(object):
    def __init__(self, x, y, reachable):
        #start a new Node
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0 # the cost to move from the starting Node to another one
        self.h = 0 # the estimated cost to move to the end
        self.f = 0 # f = g+h

    def __lt__(self, other):
        #to prevent self.f error
        return self.f < other.f

class AStar(object):
    def __init__(self):
        #keep Node with lowest F always on top
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.Nodes = []


    def init_grid(self, width, height, maze, start, end):
        # make grid from outside info
        # coordinates start at one. I don't like it either but it is the way it is, okay?
        self.grid_height = height  
        self.grid_width = width
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if maze [y][x] == 1:
                    reachable = False
                else:
                    reachable = True
                self.Nodes.append(Node(x, y, reachable))
        self.start = self.get_Node(*start)
        self.end = self.get_Node(*end)
        
        
    def get_heuristic(self, Node): 
        #tweak to optimize speed?
        return 10 * (abs(Node.x - self.end.x) + abs(Node.y - self.end.y))

    def get_Node(self, x, y):
        #gets Node from list
        return self.Nodes[x * self.grid_height + y]
    
    def get_adjacent_Nodes(self, Node):
        #self explanatory
        Nodes = []
        if Node.x < self.grid_width - 1:
            Nodes.append(self.get_Node(Node.x+1, Node.y))
        if Node.y > 0:
            Nodes.append(self.get_Node(Node.x, Node.y-1))
        if Node.x > 0:
            Nodes.append(self.get_Node(Node.x-1,Node.y))
        if Node.y < self.grid_height - 1:
            Nodes.append(self.get_Node(Node.x, Node.y+1))
        return Nodes    
            
    def get_trail(self):
        #here path is defined by LRUD turns 
        path = ''
        Node = self.end
        trail = [(Node.x, Node.y)]

        while Node.parent is not self.start:
            Node = Node.parent 
            trail.append((Node.x, Node.y)) #I hate tuples

        trail.append((self.start.x, self.start.y))
        trail.reverse()
        length = 0
        
        for element in trail:
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
        return path, trail

    def update_Node(self, adj, Node):
        adj.g = Node.g + 1 # made smaller
        adj.h = self.get_heuristic(adj)        
        adj.parent = Node
        adj.f = adj.h + adj.g
        
    def solve(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            f, Node = heapq.heappop(self.opened)
            self.closed.add(Node)
            if Node is self.end:
                return self.get_trail()
            adj_Nodes = self.get_adjacent_Nodes(Node)
            for adj_Node in adj_Nodes:
                if adj_Node.reachable and adj_Node not in self.closed:
                    if (adj_Node.f, adj_Node) in self.opened:
                        if adj_Node.g > Node.g + 1: #made smaller
                            self.update_Node(adj_Node, Node)
                    else:
                        self.update_Node(adj_Node, Node)
                        heapq.heappush(self.opened, (adj_Node.f, adj_Node))
                            
        
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
    a = AStar()
    a.init_grid(width, height, maze, start, end)
    path, trail = a.solve()
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
    a = AStar()
    a.init_grid(width, height, maze, start, end)
    path, trail = a.solve()
    print("solved: ")
    traildir(trail, maze)    
    print('path: ' + path) 

    
main_visual(maze_load())
