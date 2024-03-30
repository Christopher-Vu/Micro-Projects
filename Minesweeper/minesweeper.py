import random
import math


board = [[0] * 16 for _ in range(16)] # CHANGE THIS
mine_vals = random.sample(range(0, 256), 40)
mine_locations = []
for i in mine_vals:
    row = math.floor(i/16)
    col = (i%16) - 1
    if col==-1:
        col = 15 # change 16 to 15
    mine_locations.append((row, col))


'''add this stuff below if u want to see the mines 
(first line is already in carly's program)'''
print(mine_locations)
mines = [[0] * 16 for _ in range(16)]
for i in mine_locations:
    print(i[0], " ", i[1])
    mines[i[0]][i[1]] = 1
print(mines)


rowInput= int(input("Which row would you like to choose (1-16)?")) - 1
column = int(input("Which column would you like to choose (1-16)?")) - 1
board[rowInput][column] = 1
for row in board:
    print(row)