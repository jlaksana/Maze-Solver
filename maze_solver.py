"""
Maze Solver
Started 8/4/21
Finished 

Goal: To take in an image of a black and white maze and to find and mark
the shortest path from start to end.

Maze constraints:
 - black and white pixels where white is paths
 - surrounded by black walls
 - one white at top is entrance, one white at bottom is exit
 - maze can have multiple solutions


Control Flow:
1. Takes in a png file of a maze
2. Parse through pixels
3. Create a node at every junction and dead end
4. Connect nodes to adjacent nodes to create a graph
5. Implement breadth first search
6. Implement Dijkstra algorithm
7. Implement a* algorithm
8. Convert solutions from algorithm to draw solution onto maze

Notes:
 - Dijkstra and a* need a priority queue
 - learn how to store png data


 Week One Goal: Parse the maze image and create a graph representing the maze   COMPLETE
 Week Two: Implement the searching algorithms   COMPLETE
 Week Three: Tie up the components and create output



Resources:
https://www.youtube.com/watch?v=rop0W4QDOUI&list=PLpxeghl7_0IXWkeE8K-XGl2YRxqTo5IJL&index=9
https://www.youtube.com/watch?v=GazC3A4OQTE&list=PLpxeghl7_0IXWkeE8K-XGl2YRxqTo5IJL&index=10
https://www.youtube.com/watch?v=ySN5Wnu88nE&list=PLpxeghl7_0IXWkeE8K-XGl2YRxqTo5IJL&index=11
https://github.com/mikepound/mazesolving

"""

from PIL import Image
from maze import Maze
import time


def save_output(im, path, output):
    """Draws the solution path onto an output file of the maze.
    Params: image object, solution list of vertices, name of output file"""
    im = im.convert("RGB")
    pixels = im.load()

    for i in range(len(path)-1):
        cur = path[i]
        next = path[i+1]
        green = (0,255,0)

        if cur[0] == next[0]:
            # x values are equal
            for y in range(min(cur[1], next[1]), max(cur[1],next[1])+1):
                pixels[cur[0],y] = green

        elif cur[1] == next[1]:
            # y values are equal
            for x in range(min(cur[0],next[0]),max(cur[0],next[0])):
                pixels[x,cur[1]] = green

    im.save(output)



im = Image.open("mazes/tiny.png")
print("Parsing maze...")
maze = Maze(im)
print("Solving maze...")
t0 = time.time()
path = maze.bfs()

t1 = time.time()
print("Finished in %2.5f seconds"%(t1-t0))
print("Saving image...")
save_output(im,path,"solutions/tiny.png")