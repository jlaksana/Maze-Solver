"""
Maze Solver
Started 8/4/21
Finished 8/12/21

Goal: To take in an image of a black and white maze and to find and mark
the path from start to end.

I have always loved mazes as a kid. One of the reasons I became interested in computer
science is a computer's ability to solve mazes on its own. In this project, I built a program
that solves a maze (with the constraints written below) with a selection for four different
path finding algorithms: DFS, BFS, Dijkstra, and A Star. I was inspired to finally make this project
after watching Computerphile's video on maze solving by Dr. Mike Pound. 

Maze constraints:
 - Maze is a png image. Does not need to be square
 - black and white pixels where white is paths
 - surrounded by black walls
 - one white at top is entrance, one white at bottom is exit
 - maze can have multiple solutions

Instructions:
 1. Have Python 3.6 or later and the Pillow module installed
 2. Put image of maze in the mazes folder
 3. Run the file maze_solver.py
 4. Input the name of the file. Wait for program to parse the maze
 5. Input the name of the algorithm you want to use (dfs, bfs, dijkstra, or astar)
 6. Wait for program to solve.
 7. Open solution file from solutions folder to view solution.

Notes:
 - This project was inspired and adapted from Dr. Mike Pound's version.
 - All test mazes were downloaded from Dr. Mike Pound's version. Github link below
 - DFS and BFS generally performs faster than Dijkstra and A Star but also do not give the shortest path
 - The combo6k maze best showcases the differenct between DFS and A Star
 - Not all solutions for every algorithm for every maze are included in this repository

Resources:
https://youtu.be/rop0W4QDOUI 
https://youtu.be/GazC3A4OQTE 
https://youtu.be/ySN5Wnu88nE 
https://github.com/mikepound/mazesolving

"""

from typing import List, Set
from PIL import Image
from maze import Maze
import time


def save_output(im, path: List, output: str) -> None:
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

def ask_question(prompt: str, acceptable_reponses: Set) -> str:
    """Asks user to input an answer based on a prompt. Exits program if there are three bad attempts.
    Params: Question prompt and set of acceptable responses.
    Returns the inputted answer if acceptable"""
    answer = input(prompt)
    
    bad_ans = 0
    while not(answer.lower() in acceptable_reponses):
        bad_ans += 1
        if bad_ans == 3:
            print('Sorry, we cannot help you here.')
            quit()
      
        print('Can you please try again:')
        answer = input(prompt)            
        
    return answer

def main() -> None:
    print("-----Maze Solver-----\n")
    
    im = None
    while im is None:
        png = input("Enter name of maze: ")
        try:
            im = Image.open("mazes/" + png)
        except:
            print("Invalid image file name. Try again")
    
    
    print("Parsing maze...")
    t0 = time.time()
    try:
        maze = Maze(im)
    except:
        print("Error: Could not parse maze. Check validity of maze.")
        quit()
    t1 = time.time()
    print("Finished parsing in %2.5f seconds"%(t1-t0))

    alg = ask_question("What algorithm do you want to use? ", set(["dfs", "bfs", "dijkstra", "astar"]))
    print("Solving maze...")
    t0 = time.time()
    if alg == "dfs":
        path = maze.dfs()
    elif alg == "bfs":
        path = maze.bfs()
    elif alg == "dijkstra":
        path = maze.dijkstra()
    else:
        path = maze.astar()
    t1 = time.time()
    print("Finished solving in %2.5f seconds"%(t1-t0))

    print("Saving image...")
    save_output(im,path,"solutions/" + png[:-4] + "_sol_" + alg.lower() + ".png")
    print("End of program.\n")

if __name__ == "__main__":
    main()
