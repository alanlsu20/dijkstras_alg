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
    print("Shortest path from {} to {}:" .format(start,end))
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
    
def dijkstra(grid,start):
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
    print("Shortest path to all points in grid calculated using Dijkstra's Algorithm.")
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
        if end in grid.nodes() or end=='all':
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
                if grid.nodes()[i]!=start:
                    print(grid.nodes()[i])
                    
def test():
    """Test with example 1 in grid.py"""
    grid=g.truegrid('grid2.txt')
    g.gridprinter(grid)
    dijkstra(grid,(0,0))

def test2():
    """Test with example 2 in grid.py"""
    grid=g.example2()
    dijkstra(grid, '0')
    
                    
            
                    
    
    
        