from collections import deque
from typing import List, Any
from priorityqueue import PriorityQueue
from PIL import Image
import math


class Maze:
    """Maze Class
    Creates a graph representation of a maze image"""
    def __init__(self, im: Image) -> None:
        """Param: image object"""
        pixels = list(im.getdata(0))
        width, height = im.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        
        # keys are position tuples (x,y)
        self.adjacencyList = {}
        self.num_items = 0
        self.start = None
        self.end = None

        # algorithm adapted from Dr. Mike Pound
        topVerts = [None] * width

        #first row
        for x in range(1,width-1):
            if pixels[0][x] == 1:
                self.start = (x,0)
                self.addVertex(self.start)
                topVerts[x] = self.start
                self.num_items += 1
                break

        #body of maze
        for y in range(1,height-1):
            leftVert = None

            for x in range(1,width-1):
                prev = pixels[y][x-1]
                cur = pixels[y][x]
                next = pixels[y][x+1]
                above = pixels[y-1][x]
                below = pixels[y+1][x]
                vert = None

                if cur == 0:
                    # on wall
                    continue

                if prev > 0:
                    if next > 0:
                        # path path path
                        if above > 0 or below > 0:
                            # add only if clear above or below aka junction
                            vert = (x,y)
                            self.addVertex(vert)
                            self.addEdge(vert, leftVert)
                            leftVert = vert
                    else:
                        # path path wall
                        # can be end of path or a junction, add for both
                        vert = (x,y)
                        self.addVertex(vert)
                        self.addEdge(vert, leftVert)
                        leftVert = None
                else:
                    if next > 0:
                        # wall path path
                        # start of path or junction, add for both
                        vert = (x,y)
                        self.addVertex(vert)
                        leftVert = vert
                    else:
                        # wall path wall
                        # vertical path, add if dead end
                        if above == 0 or below == 0:
                            vert = (x,y)
                            self.addVertex(vert)

                # connect vert above or below
                if vert is not None:
                    if above > 0:
                        #clear above
                        self.addEdge(vert, topVerts[x])

                    if below > 0:
                        topVerts[x] = vert
                    else:
                        topVerts[x] = None
                    
                    self.num_items += 1

        # Find end
        for x in range(1,width-1):
            if pixels[height-1][x] == 1:
                self.end = (x,height-1)
                self.addVertex(self.end)
                self.addEdge(self.end, topVerts[x])
                self.num_items += 1
                break

        self.width = width
        self.height = height

    def addVertex(self, vertex: tuple) -> None:
        """Adds given vertex key to adjacency list. Sets default value to an empty dictionary"""
        self.adjacencyList[vertex] = {}

    def addEdge(self, source: tuple, dest: tuple):
        """Adds an edge to the source and destination vertexes. Calculates the weight and 
        updates adjacency list. Assumes both vertexes are already in the graph"""
        dx = source[0] - dest[0]
        dy = source[1] - dest[1]
        weight = abs(dx + dy)
        self.adjacencyList[source][dest] = weight
        self.adjacencyList[dest][source] = weight

    def _backtrace(self, table: dict) -> List:
        """Takes a dictionary with node keys and its previous node as a value.
        Returns a list of vertices in the order of the solution path
        O(n) time where n is the number of items in the solution path"""
        front = self.end
        res = deque()
        res.append(self.end)
        while front != self.start:
            res.appendleft(table[front])
            front = res[0]
        return res

    def dfs(self) -> List:
        """Depth-First Search algorithm.
        Returns the solution path a list of vertices
        Opted for iterative over recursive implementation because larger mazes
        often exceed recursion limit
        O(V+E) time"""
        stack = []
        visited = set()
        prev ={}

        stack.append(self.start)
        while stack:
            cur = stack.pop()
            visited.add(cur)

            if cur == self.end:
                break

            for vert in self.adjacencyList[cur].keys():
                if vert not in visited:
                    stack.append(vert)
                    prev[vert] = cur

        return self._backtrace(prev)                  

    def bfs(self) -> List:
        """Breadth-First Search algorithm.
        Returns the solution path a list of vertices
        O(V+E) time"""
        q = deque()
        visited = set()
        q.append(self.start)
        prev = {}

        while q:
            cur = q.popleft()
            visited.add(cur)

            if cur == self.end:
                break
            
            for vert in self.adjacencyList[cur].keys():
                if vert not in visited:
                    q.append(vert)
                    prev[vert] = cur

        return self._backtrace(prev)
        
    def dijkstra(self) -> List:
        """Dijkstra's shortest path algorithm using a priority queue.
        Returns a list of vertices in order of the solution path
        O(ElogV)"""
        dist = {v:math.inf for v in self.adjacencyList.keys()}
        source = dict()
        visited = set()
        pq = PriorityQueue(self.num_items*3) 

        pq.enqueue(self.start, 0)
        dist[self.start] = 0

        while not(pq.is_empty()):
            u = pq.dequeue()
            if u == self.end:
                break
            visited.add(u)
            for vert, weight in self.adjacencyList[u].items():
                if vert not in visited and dist[vert] > dist[u] + weight:
                    dist[vert] = dist[u] + weight
                    source[vert] = u
                    pq.enqueue(vert, dist[vert])
        
        return self._backtrace(source)

    def astar(self) -> List:
        """A Star Search Algorithm using a priority queue.
        Heuristic used is the Manhattan distance between a vertex to the end of the maze.
        Returns a list of vertices in order of the solution path
        O(ElogV), generally performs better than Dijkstra"""
        dist = {v:math.inf for v in self.adjacencyList.keys()}
        heur = {}
        source = dict()
        visited = set()
        pq = PriorityQueue(self.num_items*2) 

        pq.enqueue(self.start, 0)
        dist[self.start] = 0

        while not(pq.is_empty()):
            u = pq.dequeue()
            if u == self.end:
                break
            visited.add(u)
            for vert, weight in self.adjacencyList[u].items():
                if vert not in visited and dist[vert] > dist[u] + weight:
                    dist[vert] = dist[u] + weight
                    source[vert] = u
                    if vert not in heur:
                        heur[vert] = self.manhattan_dist(vert, self.end)
                    pq.enqueue(vert, dist[vert] + heur[vert])
        
        return self._backtrace(source)

    def manhattan_dist(self, source: tuple, end: tuple) -> float:
        """Finds the manhattan distance between two points given as tuples (x,y)
        Returns distance as a float"""
        return abs(source[0] - end[0]) + abs(source[1] - end[1])
