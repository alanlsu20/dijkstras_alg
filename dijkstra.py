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
    if all(value==True for value in visited.values()):
        return 
    for i in range(len(grid.adj(current))):
        c=grid.adj(current)[i]
        totaldist=grid.dist(current)[i]+distlist[current]
        if totaldist<distlist[c]:
            distlist[c]=totaldist
            pathlist[c]=current
        elif totaldist==distlist[c]:
            if type(pathlist[c])==list:
                pathlist[c].append(current)
            else:
                pathlist[c]=[pathlist[c],current]
    visited[current]=True
    #sorting adjecents by distance form start
    tempdist=[]
    tempkey=[]
    sortlist=[]
    for i in range(len(grid.adj(current))):
        tempkey.append(grid.adj(current)[i])
    tempdist=[distlist[value] for value in tempkey]
    sortlist=sorted(zip(tempdist,tempkey))
    #calling unvisited nodes recursively by increasing distance
    for i in range(len(sortlist)):
        if visited[sortlist[i][1]]==False:
            dijkstra_alg(sortlist[i][1],visited,pathlist,distlist, grid) #recursively runs dijkstra_alg until all nodes visited

def path_printer(start,end,pathlist,distlist):
    print("\nShortest path from {} to {}:" .format(start,end))
    if start==end:
        print("Start and end points are the same. Path is trivial.")
        return
    current=end
    while current!=start:
        if current==end:
            travelpath=str(current)
        else:
            travelpath=str(current)+" -> "+travelpath
        current=pathlist[current]
    travelpath=str(start)+" -> "+travelpath
    print(travelpath)
    print("Length is: {}" .format(distlist[end]))
    
def dijkstra(grid, start, avoid = None):
    """ 
    find shortest path using dijkstra's algorith from a starting node on a
    grid (will be prompted for endpoint later). Also can specify any nodes you
    wish to avoid (allowed to be list of multiple nodes)
    """
    
    if avoid != None:
        if len(avoid) > 1:
            for node in avoid:
                grid.avoid(node)
        else:
            grid.avoid(avoid)
    else:
        avoid = [None]
    
    if start not in grid.nodes():#needs to be integrated
        return "Not acceptable input, try again."
    #initializing pathlist and distlist and visited
    visited={}
    for i in range(grid.size()):
        visited[str(grid.nodes()[i])]=False
    pathlist={}
    for i in range(grid.size()):
        pathlist[str(grid.nodes()[i])]=None
    distlist={}
    for i in range(grid.size()):
        if grid.nodes()[i]==start:
            distlist[str(start)]=0
        else:
            distlist[str(grid.nodes()[i])]=inf
    dijkstra_alg(start,visited,pathlist,distlist,grid)
    #print("pathlist {}" .format(pathlist)) #to check. to be removed
    #print("distlist {}" .format(distlist)) #to check. to be removed
    print("\nShortest path to all points in grid calculated using Dijkstra's Algorithm.")
    print(f"You are avoiding the follwing points: {avoid}")
    flag=True
    while flag==True:
        end=str(input("Where do you want to go from {}?: ".format(start)))
        if end in avoid or end == avoid:
            print("You can not go to the node you are avoiding")
            print("Acceptable inputs are:")
            for i in range(grid.size()):
                if grid.nodes()[i]!= start and grid.nodes()[i] not in avoid and grid.nodes()[i] != avoid:
                    print(grid.nodes()[i])
        elif end in grid.nodes():
            path_printer(start,end,pathlist,distlist)
            print("")
            marker=input("Try another point? (input n to exit): ")
            if marker=="n":
                flag=False
        else:
            print("Input not understood. Try entering the name of a node or 'all' to print all shortest paths. You don't need to input in string format.")
            print("Acceptable inputs are:")
            for i in range(grid.size()):
                if grid.nodes()[i]!= start and grid.nodes()[i] not in avoid and grid.nodes()[i] != avoid:
                    print(grid.nodes()[i])
                    
def test():
    """Test with example 1 in grid.py"""
    grid=g.example1()
    print(f"Here is the grid for this example: \n{grid}") 
    print("\nNow we will run Dijkstra's Algorithm.")
    #check with endpoint 'E' to get path of C -> A -> E
    dijkstra(grid,'C') 
    #this time avoid 'A' but still have endpoint 'E' to get path of C -> B -> E
    dijkstra(grid, 'C', avoid = 'A') 

def test2():
    """Test with example 2 in grid.py"""
    grid=g.example2()
    print(f"Here is the grid for this example: \n{grid}") 
    print("\nNow we will run Dijkstra's Algorithm.")
    #check with endpoint '3' to get path 0 -> 1 -> 2 -> 3
    dijkstra(grid, '0')
    #this time avoid '1' with endpoint 3 to get path 0 -> 7 -> 6 -> 5 -> 2 -> 3
    dijkstra(grid, '0', avoid = '1')
    #this time avoid vectorized ['1', '6'] to get path 0 -> 7 -> 8 -> 2 -> 3
    dijkstra(grid, '0', avoid = ['1', '6'])
    
                    
            
                    
    
    
        