import Create_Board
import random
import copy
import time
import multiprocessing
global solutions
def remove_value(board, return_cords=False):
    '''
    removes number from random cell
    '''
    while True:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        if board.get(x, y) != '.':
            board.set(x, y, '.')
            if return_cords == True:
                return x, y
            else:
                return board
        
def find_empty_cell(board, used_cords=[]):
    '''
    finds empty cell scans from column to column
    '''
    value_used = False
    for x in range(9): # scan columns
        for y in range(9): # scan rows
            number = board.get(x, y) # grab value at cords
            
            if number == '.': # empty cell
                for i in used_cords: # see if we already removed cell before so it's not the new empty cell
                    if i == (x, y):
                        value_used = True
                        break

                if value_used != True: # value not used before so this is the new cell we emptied
                    return x, y 
    
    return -1, -1
        
def check_squares(board):
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

def check_rows(board):
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

def check_columns(board):
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

def Check_Board_valid(board):
    '''
    checks if current state of board still meets rules of Sudoku, returns true if board meets rules
    '''
    if check_squares(board) == False:
        return False
    if check_rows(board) == False:
        return False
    if check_columns(board) == False:
        return False
    
    return True


def solver(board):
    '''
    attempts to solve board with the passed in board, returns how many solutions it finds up to 2
    '''
    global solutions
    if solutions > 1:
        return
    x, y = find_empty_cell(board)
    if x and y == -1:
        return True
    
    
    x, y = find_empty_cell(board)
    for i in range(1, 10):
        board.set(x, y, i)
        
        if Check_Board_valid(board) == True:
            board_copy = copy.deepcopy(board)
            if solver(board_copy) == True:
                solutions += 1
            del board_copy
            


def generate_difficulty(board, difficulty, result_queue):
    '''
    used to generate difficult board from solved board

    args:
        board (grid object): pass into solved board object into here
        difficulty (int): 1 for easy, 2 for medium, 3 for hard
        result_queue: pass this to allow multiple processes to communicate
    '''
    original_board = copy.deepcopy(board)
    match difficulty:
        case 1:
            cells_range = [45]
            cells = 45
        case 2:
            cells_range = [54]
            cells = 54
        case 3:
            cells_range = [55, 56, 57, 58, 59, 60, 61, 62]
            cells = 62

    
    global solutions
    removed_values_cords = []
    removed_values = 0
    while removed_values < cells:
        x, y = remove_value(board, return_cords=True)
        board.set(x, y, '.') # first remove a cell
        removed_values_cords.append((x, y)) # add removed cell cords to list of cord for all cells removed

        removed_values += 1

        solutions = 0
        board_copy = copy.deepcopy(board)
        solver(board_copy)
        del board_copy
        if solutions != 1: # more or less than one solution exist so we try a different cell
            attempts += 1
            removed_values -= 1
            del removed_values_cords[removed_values]
            board.set(x, y, original_board.get(x, y))# restore original value of cell
            if attempts >= 5:
                if cells_range.count(removed_values) == 1:
                    break
                attempts = 0
                removed_values -= 1
                x, y = removed_values_cords[removed_values]
                board.set(x, y, original_board.get(x, y))
                del removed_values_cords[removed_values]
        else:
            attempts = 0

    result_queue.put(board)
        

    
def create_difficulty(board, difficulty):
    '''
    Function to create a puzzle from fully solved board.

    args:
        board (grid object): pass solved board object into here
        difficulty (int): 1 for easy, 2 for medium, 3 for hard
    '''
    if difficulty not in range(1, 4):
        print("please enter valid difficulty (1-3)")
        raise ValueError
    

    num_cores = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    process = []

    for i in range(num_cores):
        process.append(multiprocessing.Process(target=generate_difficulty, args=(board, difficulty, result_queue)))
    
    for i in range(num_cores):
        process[i].start()

    board = result_queue.get()

    for i in range(num_cores):
        process[i].kill()


    return board



def main():
    board = Create_Board.create_board()
    print("original board")
    print(board)
    start_time = time.perf_counter()
    board = create_difficulty(board, 3)
    stop_time = time.perf_counter()
    final_time = stop_time - start_time
    print(f'final board! Finished in {final_time:.6f} seconds!')
    print(board)






if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()