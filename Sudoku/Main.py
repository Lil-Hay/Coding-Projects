import grid
import random
from os import system
from time import sleep, perf_counter
board = grid.Grid(9, 9, ".")


def not_used(x, y):
    if board.get(x, y) == ".":
        return True
    else:
        return False
    
def create_colum(x):
    options = [1,2,3,4,5,6,7,8,9]
    for y in range(9):
        number = random.choice(options)
        board.set(x, y, number)
        options.remove(number)

def check_row(y):
    options = [1,2,3,4,5,6,7,8,9]
    for x in range(9):
        number = board.get(x, y)
        if number != ".":
            if options.count(number) == 0:
                return False
            else:
                options.remove(number)
    return True

def Squares_valid():
    Square_x = 0
    Square_y = 0
    while True:
        options = [1,2,3,4,5,6,7,8,9]
        for x in range(3):
            for y in range(3):
                number = board.get(x + Square_x, y + Square_y)
                if number != '.':
                    if options.count(number) == 0:
                        return False
                    else:
                        options.remove(number)

        if Square_y == 6:
            return True
        
        if Square_x == 6:
            Square_x = 0
            Square_y += 3
        else:
            Square_x += 3    
    
attempts = 0



x = 0
start_time = perf_counter()
while True:
    create_colum(x)
    retry = False
    if Squares_valid() == False:
        retry = True
    if retry == False:
        for y in range(9):
            if check_row(y) == False:
                retry = True
    if x == 8 and retry == False:
        break
    if retry == True:
        attempts += 1
        if x >= 5 and attempts >= 100000:
            attempts = 0
            for x in range(9):
                for y in range(9):
                    board.set(x, y, ".")
            x = 0

         
                 
    if retry == False:
        attempts = 0
        x += 1
stop_time = perf_counter()
result_time = stop_time - start_time
system('cls')
print(board)
print(f'\nIt took: {result_time:.6f} seconds')