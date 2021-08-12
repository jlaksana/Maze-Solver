# Maze-Solver

I have always loved mazes as a kid. One of the reasons I became interested in computer
science is a computer's ability to solve mazes on its own. In this project, I built a program
that solves a maze (with the constraints written below) with a selection for four different
path finding algorithms: DFS, BFS, Dijkstra, and A Star. This project allowed me to better understand
graph algorithms and working with images. I was inspired to finally make this project
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
