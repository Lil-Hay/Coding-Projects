import random
import grid
board = grid.Grid(9, 9, ".")

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

           