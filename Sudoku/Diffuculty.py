import Create_Board
import random
import grid
import copy
global board
global orignal_board
def remove_value():
    '''
    removes number from random cell
    '''
    while True:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        if board.get(x, y) != '.':
            board.set(x, y, '.')
            return
        
def find_empty_cell():
    '''
    finds empty cell scans from colum to colum
    '''
    for x in range(9):
        for y in range(9):
            number = board.get(x, y)
            if number == '.':
                return x, y
            
    return False, False
        
def check_squares():
    '''
    returns False if 3x3 square has duplicate
    '''    
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

def check_rows():
    '''
    returns false if row has duplicate
    '''
    for x in range(9):
        options = [1,2,3,4,5,6,7,8,9]
        for y in range(9):
            number = board.get(x, y)
            if number != '.':
                if options.count(number) == 0:
                    return False
                else:
                    options.remove(number)
    return True

def check_columns():
    '''
    returns false if column has duplicate
    '''
    for y in range(9):
        options = [1,2,3,4,5,6,7,8,9]
        for x in range(9):
            number = board.get(x, y)
            if number != '.':
                if options.count(number) == 0:
                    return False
                else:
                    options.remove(number)
    return True

def Check_Board_valid():
    '''
    checks if current state of board still meets rules of Sudoku, returns true if board meets rules
    '''
    if check_squares() == False:
        return False
    if check_rows() == False:
        return False
    if check_columns() == False:
        return False
    
    return True






#def possible_answers():
    




def generate_diffuculty():
    # how many cells to remove determined by this variable
    removed_values = 0
    while removed_values < 19: # for easy diffuculty
        remove_value() # first remove a cell

        print("removed one element")
        print(board)


        removed_values += 1

        x, y = find_empty_cell() # find first empty cell

        # find value that satisfy's rules 
        for i in range(9):
            board.set(x, y, i+1)            
            if Check_Board_valid() == True:
                break

    print("solved removed element")
    print(board)
    print("orignal_board")
    print(orignal_board)





def create_board():
    '''
    creates two boards one that all functions munipulate, one that is a refrence
    '''
    global board, orignal_board
    board = Create_Board.create_board()
    orignal_board = copy.deepcopy(board)
    
    


def main():
    create_board()
    generate_diffuculty()






if __name__ == '__main__':
    main()