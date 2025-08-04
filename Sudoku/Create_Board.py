from os import system
from time import perf_counter
import multiprocessing
import grid
import random

    
def create_colum(board, x):
    options = [1,2,3,4,5,6,7,8,9]
    for y in range(9):
        number = random.choice(options)
        board.set(x, y, number)
        options.remove(number)
    return board

def check_row(board, y):
    options = [1,2,3,4,5,6,7,8,9]
    for x in range(9):
        number = board.get(x, y)
        if number != ".":
            if options.count(number) == 0:
                return False
            else:
                options.remove(number)
    return True

def Squares_valid(board):
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



def generate_board(result_queue):
    
    board = grid.Grid(9, 9, ".")
    attempts = 0
    x = 0
    while True:
        board = create_colum(board, x)
        retry = False

        if Squares_valid(board) == False:
            retry = True

        if retry == False:
            for y in range(9):
                if check_row(board, y) == False:
                    retry = True

        if x == 8 and retry == False:
            result_queue.put(board)
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

def create_board():
    '''
    function that creates a Sudoku board with all cells filled in meeting all rules
    '''

    num_cores = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    process = []

    for i in range(num_cores):
        process.append(multiprocessing.Process(target=generate_board, args=(result_queue,)))
    
    for i in range(num_cores):
        process[i].start()

    board = result_queue.get()

    for i in range(num_cores):
        process[i].kill()

    return board

def main():
    system('cls')
    start_time = perf_counter()
    board = create_board()
    stop_time = perf_counter()
    final_time = stop_time - start_time
    print(board)
    print(f'Finished in {final_time:.6f} seconds!')


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()




