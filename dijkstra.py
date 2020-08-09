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
    #sorting adjecents by distance from start
    tempdist=[]
    tempkey=[]
    sortlist=[]
    for i in range(len(grid.adj(current))):
        tempkey.append(grid.adj(current)[i])
    tempdist=[distlist[value] for value in tempkey]
    sortlist=sorted(zip(tempdist,tempkey))
    #calling unvisited nodes recursively by increasing distance
    for i in range(len(tempkey)):
        if visited[sortlist[i][1]]==False:
            dijkstra_alg(sortlist[i][1],visited,pathlist,distlist, grid) #recursively runs dijkstra_alg until all nodes visited

def path_printer(start,end,pathlist,distlist):
    """Prints paths found recursively in rpath"""
    print("\nShortest path from {} to {}:" .format(start,end))
    if start==end:
        print("Start and end points are the same. Path is trivial.")
        return
    travelpath=[" "]
    rpath(start,end,pathlist,distlist,travelpath, 0)
    for i in range(len(travelpath)):
        print("Path {}: {}".format(i+1,travelpath[i]))
    print("Length is: {}" .format(distlist[end]))

def rpath(start,current,pathlist,distlist,travelpath,index):
    """Recursively finds all shortest paths between two nodes. Accounts for
    all permutations of ties in distance."""
    if current==start:
        travelpath[index]=str(start)+travelpath[index]
        return 
    indexlist=[]
    if type(pathlist[current])==list:
        for i in range(len(pathlist[current])-1): #adding new lists
            travelpath.append(" -> "+str(current)+travelpath[index]) #copying work of this list
            indexlist.append(len(travelpath)-1)
        travelpath[index]=" -> "+str(current)+travelpath[index] #adding entry to list
        for i in range(len(pathlist[current])):
            if i==(len(pathlist[current])-1):
                rpath(start,pathlist[current][i],pathlist,distlist,travelpath,index)
            else:
                rpath(start,pathlist[current][i],pathlist,distlist,travelpath,indexlist[i])
    else:
        travelpath[index]=" -> "+str(current)+travelpath[index]
        rpath(start,pathlist[current],pathlist,distlist,travelpath,index)
        
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
        visited[grid.nodes()[i]]=False
    pathlist={}
    for i in range(grid.size()):
        pathlist[grid.nodes()[i]]=None
    distlist={}
    for i in range(grid.size()):
        if grid.nodes()[i]==start:
            distlist[start]=0
        else:
            distlist[grid.nodes()[i]]=inf
    dijkstra_alg(start,visited,pathlist,distlist,grid)
    #print("pathlist {}" .format(pathlist)) #to check. to be removed
    #print("distlist {}" .format(distlist)) #to check. to be removed
    print("\nShortest path to all points in grid calculated using Dijkstra's Algorithm.")
    print(f"You are avoiding the following points: {avoid}")
    flag=True
    while flag==True:
        tempinp=input("Where do you want to go from {}?:" .format(start))
        if tempinp=='all':
            end=tempinp
            for i in range(grid.size()):
                if grid.nodes()[i]!=start:
                    print("{}: " .format(grid.nodes()[i]), end="")
                    path_printer(start,grid.nodes()[i],pathlist,distlist)
                    print("")
        elif type(grid.nodes()[0])==tuple:
            tempinp=tempinp.strip('(')
            tempinp=tempinp.strip(')')
            tempinp=tempinp.split(',')
            for i in range(len(tempinp)):
                tempinp[i]=int(tempinp[i])
                end=tuple(tempinp)
        elif type(grid.nodes()[0])==int:
            end=int(tempinp)
        else: #includes strings
            end=tempinp
        if end in avoid or end == avoid:
            print("You can not go to the node you are avoiding")
            print("Acceptable inputs are:")
            for i in range(grid.size()):
                if grid.nodes()[i]!= start and grid.nodes()[i] not in avoid and grid.nodes()[i] != avoid:
                    print(grid.nodes()[i])
        elif end in grid.nodes() or end=='all':
            if end!='all':
                path_printer(start,end,pathlist,distlist)
                print("")
            while True:
                marker=input("Try another point? (y/n):")
                if marker=="n":
                    flag=False
                    break
                if marker=='y':
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
    
def rprinttest():
    """Demonstrates recursive pathfinder that accounts for multiple shortest
    paths. Generates grid from grid2.txt file."""
    grid=g.truegrid('grid1.txt')
    g.gridprinter(grid)
    dijkstra(grid,(0,0))
                    
            
                    
    
    
        