import numpy as np
import random as rr
import matplotlib.pyplot as plt
import os
import sys
import shutil
import multiprocessing
import glob
import IPython

def backTrackerMaze(number, width=101, height=101):
    shape = (height, width)
    # Build actual maze
    Z = np.ones(shape, dtype=bool)  # Maze-grid: 1's are black, 0's are white

    # Inititally set all cells as unvisited.
    Y = np.zeros(shape, dtype=bool)  # Visted or not

    # stack of visted cells
    stack = []
    ## Recursive backtracker
    # 1 Make the initial cell the current cell and mark it as visited.
    # Random Initial cell
    A, B = rr.choice(range(0, (shape[0]), 2)), rr.choice(range(0, (shape[1]), 2))

    # Making it the current cell
    Z[A][B] = 0
    # Marking it as visited
    Y[A][B] = 1
    stack.append([A, B])

    # 2 While there are unvisited cells
    while (not Y.all()):
        # print(A,B)
        # 2.1 If the current cell has any neighbors which have not been visited
        nebs = []
        walls = []

        if A + 2 in range(height) and Y[A + 2][B] == 0:
            nebs.append([A + 2, B])
            walls.append([A + 1, B])
        if A - 2 in range(height) and Y[A - 2][B] == 0:
            nebs.append([A - 2, B])
            walls.append([A - 1, B])
        if B + 2 in range(width) and Y[A][B + 2] == 0:
            nebs.append([A, B + 2])
            walls.append([A, B + 1])
        if B - 2 in range(width) and Y[A][B - 2] == 0:
            nebs.append([A, B - 2])
            walls.append([A, B - 1])
        if nebs:
            # 2.1.1 Choose randomly one of the unvisited neighbors
            cho = rr.choice(range(len(nebs)))
            # 2.1.2 Push the current cell to the stack
            stack.append([A, B])
            # 2.1.3 Remove the wall between the current cell and the chosen cell
            Z[nebs[cho][0]][nebs[cho][1]] = 0
            Z[walls[cho][0]][walls[cho][1]] = 0
            # 2.1.4 Make the chosen cell the current cell and mark it as visited
            A = nebs[cho][0]
            B = nebs[cho][1]
            Y[nebs[cho][0]][nebs[cho][1]] = 1
            Y[walls[cho][0]][walls[cho][1]] = 1

            stack.append([A, B])
        # 2.2. Else if stack is not empty
        elif stack:
            if A + 1 in range(height):
                Y[A + 1][B] = 1
            if A - 1 in range(height):
                Y[A - 1][B] = 1
            if B + 1 in range(width):
                Y[A][B + 1] = 1
            if B - 1 in range(width):
                Y[A][B - 1] = 1
            # 2.2.1 Pop a cell from the stack
            p = stack.pop()
            # 2.2.2 Make it the current cell
            A = p[0]
            B = p[1]
        else:
            break

    plt.figure()
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.savefig("pics/backTrackerMazes/backTrackerMaze{0:0=2d}.png".format(number))
    np.savetxt("arrs/backTrackerMazes/{0:0=2d}.txt".format(number), Z, fmt='%d')

def randGridMaze(number, width=101, height=101):
    shape = (height, width)
    Z = np.random.choice([0, 1], size=shape, p=[.70, .30])
    plt.figure()
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.savefig("pics/randGrid/maze{0:0=2d}.png".format(number))
    np.savetxt("arrs/randGrid/{0:0=2d}.txt".format(number), Z, fmt='%d')

if __name__ == "__main__":
    if os.path.exists("arrs"):
        shutil.rmtree("arrs")
    if os.path.exists("pics"):
        shutil.rmtree("pics")
    if os.path.exists("maze.png"):
        os.remove("maze.png")

    for i in ["", "/backTrackerMazes/", "/randGrid/"]:
        os.mkdir("pics" + i)
        os.mkdir("arrs" + i)

    ### specify the number of grids you want to generate
    n_grids = int(sys.argv[1])

    multiprocessing.freeze_support()
    num_proc = multiprocessing.cpu_count()
    ## for python 3.6 uncomment the line below, and comment the line above
    # num_proc = os.cpu_count()
    pool = multiprocessing.Pool(processes=num_proc)

    nn = [i for i in range(n_grids)]
    pool.map(randGridMaze, nn)

    nn = [i + n_grids for i in nn]
    pool.map(backTrackerMaze, nn)

    pool.close()
    pool.join()