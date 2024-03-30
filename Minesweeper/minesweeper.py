import random
import math


board = [[0]*16]*16
mines = [[0]*16]*16
mine_vals = random.sample(range(0, 256), 40)
mine_locations = []
for i in mine_vals:
    row = math.floor(i/16)
    col = (i%16) - 1
    if col==-1:
        col = 16
    mine_locations.append((row, col))
print(mine_locations)


rowInput= int(input("Which row would you like to choose (1-16)?")) - 1
column = int(input("Which column would you like to choose (1-16)?")) - 1
board[rowInput][column] = 1
for row in board:
    print(row)