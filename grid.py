"""
MATH260 Final Project
Dijkstra's Algorithm for Shortest Path Optimization
Authors: Alan Su and Peter Holmes
"""

from math import inf
from string import ascii_uppercase as caps

class Grid:
    def __init__(self, node_list, num, gridsize='N/A'):
        keys = [node_list[i] for i in range(num)]
        grid = {}
        
        for i in keys:
            grid[i] = {"adj": [], "dist": []}   
            
        self.grid = grid
        self.gridsize = gridsize
        
    def __repr__(self):
        rep = ""
        
        for key in self.grid:
            rep += f"\n{key}: {self.grid[key]}"
        
        return rep
                 
    def edge(self, node1, node2, distance = 12):
        """ 
        Specify a connection between two nodes, and their distance if desired. 
        If distance not input will be assigned value of '10'
        """
        
        g = self.grid
     
        if node1 in g and node2 in g and node1 != node2:      
            g[node1]['adj'].append(node2)
            g[node1]['dist'].append(distance)
            
            g[node2]['adj'].append(node1)
            g[node2]['dist'].append(distance)
        else:
            raise KeyError("Input names of two different existing nodes")
            
    def fill(self):
        """ Auto-fills all remaining possible connections betweeen nodes """
        nodes = self.nodes()
        g = self.grid
        
        for node1 in nodes:
            for node2 in nodes:
                if node2 not in g[node1]['adj'] and node1 != node2:
                    self.edge(node1, node2)

    def nodes(self):
        """ Return list of all nodes within Grid class """
        node_list = []
        
        for key in self.grid.keys():
            node_list.append(key)  
            
        return node_list
       
    def size(self):
        """ Return size of Grid class """
        return len(self.grid)   
              
    def adj(self, node):
        """ Return all adjacencies of an inputted node """
        return self.grid[node]['adj']
    
    def dist(self, node):
        """ Return all distances from an inputted node """
        return self.grid[node]['dist']
    
    def dist2(self, node1, node2):
        """ Returns the distance bewteen two inputted nodes """
        adj1 = self.adj(node1)
        dist1 = self.dist(node1)
        adjdict = {}
        for i in range(len(adj1)):
            adjdict[adj1[i]] = dist1[i]
        if node2 in adj1:
            return adjdict[node2]
        else:
            print('Inputted nodes not adjacent.')
            
    def avoid(self, node):
        """ 
        Sets distances to and from inputted node equal to infity to ensure node
        is avoided in path finding algorithms
        """
        for i in range(len(self.dist(node))):
            self.grid[node]['dist'][i] = inf
            
        adj = self.adj(node)
        
        for x in adj:
            index = list(self.adj(x)).index(node)
            self.grid[x]['dist'][index] = inf


def truegrid(fname):
    """
    Creates a true grid from a file. Outline for file specificaitons in 
    file_reader() doc string. Print using gridprinter(). 
    """
    across, updown = file_reader(fname)
    m = len(across)
    n = len(updown[0])
    node_list = []
    for i in range(m):
        for j in range(n):
            node_list.append((i,j))
    g = Grid(node_list, m*n, (m,n))
    for i in range(m):
        for j in range(n):
            if i != (m-1):
                g.edge((i,j), (i+1,j), updown[i][j])
            if j != (n-1):
                    g.edge((i,j),(i,j+1), across[i][j])
    return g

def gridprinter(grid):
    """
    Prints grid visually in command line. Starts with (0,0) node at top left.
    (m,n) increases in n moving right across the row, increases in m moving 
    down the column.
    """
    m,n = grid.gridsize
    for i in range(m):
        for j in range(n):
            current = grid.nodes()[j+(i*n)]
            print(current, end = "")
            if j != (n-1): 
                rightnode = grid.nodes()[j+(i*n)+1]
                print("==[{:^3}]==".format(grid.dist2(current,rightnode)), end = "")
            else:
                print("")
        if i != (m-1): #if not last line
            for j in range(n):#spacing line
                print("  ||  ", end = "")
                if j != (n-1):
                    print("         ", end = "")
                else:
                    print("")
            for j in range(n):#vertical distance
                current = grid.nodes()[j+(i*n)]
                upnode = grid.nodes()[j+((i+1)*n)]
                print("[{:^4}]".format(grid.dist2(current,upnode)), end = "")
                if j != (n-1):
                    print("         ", end = "")
                else:
                    print("")
            for j in range(n):#spacing line
                print("  ||  ", end = "")
                if j != (n-1):
                    print("         ", end = "")
                else:
                    print("")           

def file_reader(fname):
    """
    File reader. Use .txt file where first row is the distances 
    between nodes horizontally, second row is the distances between nodes 
    vertically. Repeats for the size of the grid. End each line with a space.
    """
    file = open(fname, 'r')
    across = []
    updown = []
    line = file.readline()
    while line:
        data = line.split(' ')
        across.append(data)
        line = file.readline()
        if line:
            data = line.split(' ')
            updown.append(data)
        line = file.readline()
    for i in range(len(updown)): #converting to integer and popping off last blank entry
        updown[i].pop()
        for j in range(len(updown[0])):
            updown[i][j] = int(updown[i][j])
    for i in range(len(across)): #converting to integer and popping off last blank entry
        across[i].pop()
        for j in range(len(across[0])):
            across[i][j] = int(across[i][j])
    return across, updown
    

def example1(): 
    g = Grid(caps, 5)
    g.edge('A', 'B', 3)
    g.edge('A', 'C', 7)
    g.edge('A', 'E', 2)
    g.edge('B', 'C', 5)
    g.edge('B', 'D', 9)
    g.edge('B', 'E', 6)
    g.fill()
    return g

def example2():
    node_list=[]
    for i in range(9):
        node_list.append(str(i))
    g = Grid(node_list,9)
    g.edge('0','1',4)
    g.edge('0','7',8)
    g.edge('1','7',11)
    g.edge('1','2',8)
    g.edge('7','8',7)
    g.edge('7','6',1)
    g.edge('2','8',2)
    g.edge('8','6',6)
    g.edge('2','3',7)
    g.edge('2','5',4)
    g.edge('6','5',2)
    g.edge('3','5',14)
    g.edge('3','4',9)
    g.edge('5','4',10)
    return g

<<<<<<< HEAD
=======
def example3():
    g = truegrid('grid1.txt')
    return g

>>>>>>> 15040c493ae74c325b603423953846f84fc13c6a
