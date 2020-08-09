#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authors: Alan Su and Peter Holmes
"""

from math import inf
import grid as g

def dijkstra_alg(current, visited, pathlist, distlist, grid):
    """Using recursive scheme. Generates list of shortest path to every
        node from start point."""
    if all(value == True for value in visited.values()):
        return 
    for i in range(len(grid.adj(current))):
        c = grid.adj(current)[i]
        totaldist = grid.dist(current)[i] + distlist[current]
        if totaldist < distlist[c]:
            distlist[c] = totaldist
            pathlist[c] = current
        elif totaldist == distlist[c]:
            if type(pathlist[c]) == list:
                pathlist[c].append(current)
            else:
                pathlist[c] = [pathlist[c],current]
    visited[current] = True
    #sorting adjecents by distance form start
    tempdist = []
    tempkey = []
    sortlist = []
    for i in range(len(grid.adj(current))):
        tempkey.append(grid.adj(current)[i])
    tempdist = [distlist[value] for value in tempkey]
    sortlist = sorted(zip(tempdist,tempkey))
    #calling unvisited nodes recursively by increasing distance
    for i in range(len(sortlist)):
        if visited[sortlist[i][1]] == False:
            dijkstra_alg(sortlist[i][1], visited, pathlist, distlist, grid) #recursively runs dijkstra_alg until all nodes visited

def path_printer(start, end, pathlist, distlist):
    print(f"\nShortest path from {start} to {end}:")
    if start == end:
        print("Start and end points are the same. Path is trivial.")
        return
    current = end
    while current != start:
        if current == end:
            travelpath = str(current)
        else:
            travelpath = str(current) + " -> " + travelpath
        current = pathlist[current]
    travelpath = str(start) + " -> " + travelpath
    print(travelpath)
    print("Length is: {}".format(distlist[end]))

def rpath_printer(start, end, pathlist, distlist):
    print(f"\nShortest path from {start} to {end}:")
    if start == end:
        print("Start and end points are the same. Path is trivial.")
        return
    travelpath = [" "]
    rpath(start, end, pathlist, distlist, travelpath, 0)
    for i in range(len(travelpath)):
        print("Path {}: {}".format(i+1,travelpath[i]))
    print("Length is: {}".format(distlist[end]))

def rpath(start, current, pathlist, distlist, travelpath, index):
    if current == start:
        travelpath[index] = str(start) + travelpath[index]
        return 
    if type(pathlist[current]) == list:
        for i in range(len(pathlist[current])-1): #adding new lists
            travelpath.append(" -> " + str(current) + travelpath[index])
        travelpath[index] = " -> " + str(current) + travelpath[index]
        for i in range(len(pathlist[current])):
            rpath(start, pathlist[current][i], pathlist, distlist, travelpath, index+i)
    else:
        travelpath[index] = " -> " + str(current) + travelpath[index]
        rpath(start, pathlist[current], pathlist, distlist, travelpath, index)
        
def dijkstra(grid, start, avoid = None):
    """ 
    find shortest path using dijkstra's algorith from a starting node on a
    grid (will be prompted for endpoint later). Also can specify any nodes you
    wish to avoid (allowed to be list of multiple nodes)
    """
    
    if len(start) > 1:
        if avoid == None:
            avoid = [None]
        elif type(avoid) == list:
            for node in avoid:
                grid.avoid(node) 
        else:
            grid.avoid(avoid)
    elif avoid != None:
        if len(avoid) > 1:
            for node in avoid:
                grid.avoid(node)
        else:
            grid.avoid(avoid)
    else:
        avoid = [None]
    
    if start not in grid.nodes():
        return "Not acceptable input, try again."
    #initializing pathlist and distlist and visited
    visited = {}
    for i in range(grid.size()):
        visited[grid.nodes()[i]] = False
    pathlist = {}
    for i in range(grid.size()):
        pathlist[grid.nodes()[i]] = None
    distlist = {}
    for i in range(grid.size()):
        if grid.nodes()[i] == start:
            distlist[start] = 0
        else:
            distlist[grid.nodes()[i]] = inf
    dijkstra_alg(start, visited, pathlist, distlist, grid)
    print("\nShortest path to all points in grid calculated using Dijkstra's Algorithm.")
    print(f"You are avoiding the follwing points: {avoid}")
    flag = True
    while flag == True:
        tempinp = input(f"Where do you want to go from {start}?: ")
        if tempinp == 'all':
            end = tempinp
            for i in range(grid.size()):
                if grid.nodes()[i] != start:
                    print("{}: ".format(grid.nodes()[i]), end = "")
                    path_printer(start, grid.nodes()[i], pathlist, distlist)
                    print("")
        elif type(grid.nodes()[0]) == tuple:
            tempinp = tempinp.strip('(')
            tempinp = tempinp.strip(')')
            tempinp = tempinp.split(',')
            for i in range(len(tempinp)):
                tempinp[i] = int(tempinp[i])
                end = tuple(tempinp)
        elif type(grid.nodes()[0]) == int:
            end = int(tempinp)
        else: #includes strings
            end = tempinp
        if end in avoid or end == avoid:
            print("You can not go to the node you are avoiding")
            print("Acceptable inputs are:")
            for i in range(grid.size()):
                if grid.nodes()[i]!= start and grid.nodes()[i] not in avoid and grid.nodes()[i] != avoid:
                    print(grid.nodes()[i])
        elif end in grid.nodes() or end == 'all':
            if end != 'all':
                path_printer(start, end, pathlist, distlist)
                print("")
            while True:
                marker = input("Try another point? (y/n): ")
                if marker == "n":
                    flag = False
                    break
                if marker == 'y':
                    break
                else:
                    print("Input not accepted. Try again.")
        else:
            print("Input not understood. Try entering the name of a node or 'all' to print all shortest paths. You don't need to input in string format.")
            print("Acceptable inputs are:")
            for i in range(grid.size()):
                if grid.nodes()[i]!= start and grid.nodes()[i] not in avoid and grid.nodes()[i] != avoid:
                    print(grid.nodes()[i])
                    
def test():
    """Test with example 1 in grid.py"""
    grid = g.example1()
    print(f"Here is the grid for this example: \n{grid}") 
    print("\nNow we will run Dijkstra's Algorithm.")
    #check with endpoint 'E' to get path of C -> A -> E and endpoint 'all' to
    #see all possible paths
    dijkstra(grid, 'C') 
    #this time avoid 'A' but still have endpoint 'E' to get path of C -> B -> E
    dijkstra(grid, 'C', avoid = 'A') 

def test2():
    """Test with example 2 in grid.py"""
    grid = g.example2()
    print(f"Here is the grid for this example: \n{grid}") 
    print("\nNow we will run Dijkstra's Algorithm.")
    #check with endpoint '3' to get path 0 -> 1 -> 2 -> 3
    dijkstra(grid, '0')
    #this time avoid '1' with endpoint 3 to get path 0 -> 7 -> 6 -> 5 -> 2 -> 3
    dijkstra(grid, '0', avoid = '1')
    #this time avoid vectorized ['1', '6'] to get path 0 -> 7 -> 8 -> 2 -> 3
    dijkstra(grid, '0', avoid = ['1', '6'])
    
def test3():
    """ Test with example 3 in grid.py """
    grid = g.example3()
    print("Here is the grid for this example: \n")
    g.gridprinter(grid)
    print("\nNow we will run Dijkstra's Algorithm.")
    #check with endpoint (2,0) to get path:
    #(0, 0) -> (1, 0) -> (2, 0)
    dijkstra(grid, (0,0))
    #this time avoid (1,0) with endpoint (2,0) to get path:
    #(0, 0) -> (0, 1) -> (1, 1) -> (2, 1) -> (2, 0)
    dijkstra(grid, (0,0), avoid = (1,1))
    #this time avoid vectorized [(1,0), (1,1)] with endpoint (2,0) to get path:
    #(0, 0) -> (0, 1) -> (0, 2) -> (1, 2) -> (2, 2) -> (2, 1) -> (2, 0)
    dijkstra(grid, (0,0), [(1,0), (1,1)])
    
                    
    
    
        