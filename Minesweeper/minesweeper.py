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
if 1:
    print(mine_locations)
    mines = [[0] * 16 for _ in range(16)]
    for i in mine_locations:
        mines[i[0]][i[1]] = 1
    for i in mines:
        print(i)

def count_mines(mine_locations, row, col):
    if (row, col) in mine_locations:
        return "mine"

    total_mines = 0
    adjacent_spaces = [(row + 1, col + 1), (row + 1, col), (row + 1, col - 1),
                       (row, col + 1), (row, col - 1),
                       (row - 1, col + 1), (row - 1, col), (row - 1, col - 1)]
    for location in adjacent_spaces:
        try:
            if location in mine_locations:
                total_mines += 1
        except:
            continue
    return total_mines

def print_board(board):
    print("".join(["_" for _ in range(32)]))
    for row in board:
        print(" | ".join([str(col) for col in row]))
    print("".join(["-" for _ in range(32)]))

if 1:
    rowInput= int(input("Which row would you like to choose (1-16)?")) - 1
    colInput = int(input("Which column would you like to choose (1-16)?")) - 1
    print(count_mines(mine_locations, rowInput, colInput))
    print_board(mines)