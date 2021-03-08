import numpy as np
import random as rr
import matplotlib.pyplot as plt
import os
import sys
import shutil
import multiprocessing
import glob
import IPython

# Turn text file into matrix

c = 0
r = 0
matSize = 101
combStr = ""
counter = 0
mazeArr = np.zeros([matSize, matSize])

with open('01.txt', 'r') as f:
    for x in range(matSize*(matSize*2+100)):
        j = f.read(1)
        if j == "0" or j == "1":
            combStr += j

for y in range(matSize):
    for x in range(matSize):
        mazeArr[y][x] = int(combStr[counter])
        counter = counter + 1

# Create start and goal points at random blank spaces, 2 is start, 3 is goal

checkerS = 0

checkerG = 0

startX = 0

startY = 0

goalX = 0

goalY = 0

#Manuals values can be used for flipping the previous random values, triggering a Repeated Backward A* search

userIn = input("Enter random values with a or manual with b")

if userIn == "a":
    while checkerS == 0:
        num1 = rr.randint(0, 100)
        num2 = rr.randint(0, 100)
        if mazeArr[num1][num2] == 0:
            mazeArr[num1][num2] = 2
            startY = num1
            startX = num2
            checkerS = 1
            print(startY)
            print(startX)

    while checkerG == 0:
        num1 = rr.randint(0, 100)
        num2 = rr.randint(0, 100)
        if mazeArr[num1][num2] == 0:
            mazeArr[num1][num2] = 2
            goalY = num1
            goalX = num2
            checkerG = 1
            print(goalY)
            print(goalX)
if userIn == "b":
    startY = int(input("enter startY"))
    startX = int(input("enter startX"))
    goalY = int(input("enter goalY"))
    goalX = int(input("enter goalX"))

# Repeated Forward A star search for largest and smallest g value

class Node:

    def __init__(self, t, g, h, a, b):
        self.t = t
        self.g = g
        self.h = h
        self.a = a
        self.b = b
        self.branches = []
        self.parent = None

    def branchAdd(self, branch):
        branch.parent = self
        self.branches.append(branch)


visited = Node(0, 0, 0, 0, 0)

expanded = Node(0, 0, 0, 0, 0)

start = Node((abs(startX-goalX) + abs(startY-goalY)), 0, (abs(startX-goalX) + abs(startY-goalY)), startY, startX)

goal = Node((abs(startX-goalX) + abs(startY-goalY)), (abs(startX-goalX) + abs(startY-goalY)), 0, goalY, goalX)


def contained_visited(node):
    length = len(visited.branches)
    for z in range(length):
        if node.a == visited.branches[z].a and node.b == visited.branches[z].b:
            return True
    return False


# contained_expanded checks branches of already expanded objects to reroute a node if it has two parents


def contained_expanded(node):
    length = len(expanded.branches)
    for z in range(length):
        length2 = len(expanded.branches[z].branches)
        for j in range(length2):
            if expanded.branches[z].branches[j].a == node.a and expanded.branches[z].branches[j].b == node.b:
                tot = expanded.branches[z].t
                return tot


def contained_in_expanded(node):
    length = len(expanded.branches)
    for z in range(length):
        if node.a == expanded.branches[z].a and node.b == expanded.branches[z].b:
            return True
    return False


curr = start


def expansion(expand):
    numy = expand.a
    numx = expand.b

    # counter-clockwise preference starting at South, then East, North, and West

    if matSize-1 >= numy+1 >= 0:
        if mazeArr[numy+1][numx] != 1:
            t = (abs(numx-goalX) + abs(numy+1-goalY)) + (abs(numx-startX) + abs(numy+1-startY))
            g = (abs(numx-startX) + abs(numy+1-startY))
            h = abs(numx-goalX) + abs(numy+1-goalY)
            #branch = Node(t, g, h, numx, numy+1)
            branch = Node(t, g, h, numy+1, numx)
            branch_contain = contained_in_expanded(branch)
            if not branch_contain:
                visit = contained_visited(branch)
                tot = 0
                if visit:
                    tot = contained_expanded(branch)
                if expand.t >= tot:
                    branch.parent = expand
                expand.branches.append(branch)
                visited.branches.append(branch)
    if matSize-1 >= numx+1 >= 0:
        if mazeArr[numy][numx+1] != 1:
            t = (abs(numx+1-goalX) + abs(numy-goalY)) + (abs(numx+1-startX) + abs(numy-startY))
            g = (abs(numx+1-startX) + abs(numy+1-startY))
            h = abs(numx+1-goalX) + abs(numy-goalY)
            #branch = Node(t, g, h, numx+1, numy)
            branch = Node(t, g, h, numy, numx+1)
            branch_contain = contained_in_expanded(branch)
            if not branch_contain:
                visit = contained_visited(branch)
                tot = 0
                if visit:
                    tot = contained_expanded(branch)
                if expand.t >= tot:
                    branch.parent = expand
                expand.branches.append(branch)
                visited.branches.append(branch)
    if 0 <= numy-1 <= matSize-1:
        if mazeArr[numy-1][numx] != 1:
            t = (abs(numx-goalX) + abs(numy-1-goalY)) + (abs(numx-startX) + abs(numy-1-startY))
            g = (abs(numx-startX) + abs(numy-1-startY))
            h = abs(numx-goalX) + abs(numy-1-goalY)
            #branch = Node(t, g, h, numx, numy-1)
            branch = Node(t, g, h, numy-1, numx)
            branch_contain = contained_in_expanded(branch)
            if not branch_contain:
                visit = contained_visited(branch)
                tot = 0
                if visit:
                    tot = contained_expanded(branch)
                if expand.t >= tot:
                    branch.parent = expand
                expand.branches.append(branch)
                visited.branches.append(branch)
    if 0 <= numx-1 <= matSize-1:
        if mazeArr[numy][numx-1] != 1:
            t = (abs(numx-1-goalX) + abs(numy-goalY)) + (abs(numx-1-startX) + abs(numy-startY))
            g = (abs(numx-1-startX) + abs(numy-1-startY))
            h = abs(numx-1-goalX) + abs(numy-goalY)
            #branch = Node(t, g, h, numx-1, numy)
            branch = Node(t, g, h, numy, numx-1)
            branch_contain = contained_in_expanded(branch)
            if not branch_contain:
                visit = contained_visited(branch)
                tot = 0
                if visit:
                    tot = contained_expanded(branch)
                if expand.t >= tot:
                    branch.parent = expand
                expand.branches.append(branch)
                visited.branches.append(branch)
    expanded.branches.append(expand)


# smallest g-value

def find_smallest_g():
    length = len(visited.branches)
    small_g_holder = 0
    first_checker = True
    small_g = Node(0, 0, 0, 0, 0)
    for z in range(length):
        checker = contained_in_expanded(visited.branches[z])
        if (small_g_holder > visited.branches[z].t or first_checker) and not checker:
            small_g_holder = visited.branches[z].t
            small_g = visited.branches[z]
            first_checker = False
    return small_g


# largest g value

def find_largest_g():
    length = len(visited.branches)
    large_g_holder = 0
    first_checker = True
    largest_g = Node(0, 0, 0, 0, 0)
    for z in range(length):
        checker = contained_in_expanded(visited.branches[z])
        if (large_g_holder < visited.branches[z].t or first_checker) and not checker:
            large_g_holder = visited.branches[z].t
            largest_g = visited.branches[z]
            first_checker = False
    return largest_g


def print_matrix(matrix):
    plt.imshow(matrix, interpolation='nearest')
    plt.show()


user_input = input("Press a for Repeated Forward A*Star smallest-g or Press b for largest-g")

maze_arr_result = mazeArr


if user_input == "a":
    end_checker = False
    counter = 0
    while not end_checker:
        counter = counter + 1
        expansion(curr)
        curr = find_smallest_g()
        if curr.a == goalY and curr.b == goalX:
            end_checker = True
            break
        if counter == 5000:
            print(" no path")
            break
    #print(curr.a+100)
    #print(curr.b+100)
    while curr.a != startY or curr.b != startX:
        maze_arr_result[curr.a][curr.b] = 9
        curr = curr.parent
    print_matrix(maze_arr_result)
if user_input == "b":
    end_checker = False
    counter = 0
    while not end_checker:
        counter = counter + 1
        expansion(curr)
        curr = find_largest_g()
        if curr.a == goalY and curr.b == goalX:
            end_checker = True
            break
        if counter == 1000:
            print(" no path")
            break
    #print(curr.a+100)
    #print(curr.b+100)
    while curr.a != startY or curr.b != startX:
        maze_arr_result[curr.a][curr.b] = 9
        curr = curr.parent
    print_matrix(maze_arr_result)