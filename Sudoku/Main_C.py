from os import system
from time import sleep
import interact_with_C
import grid
def wrong_input(message, time=1.5, board = None):
    system('cls')
    print(message)
    sleep(time)
    system('cls')
    if board != None:
        display_board(board)

def convert_single_line_board(grid, board):
    for x in range(9):
        for y in range(9):
            grid.set(x, y, board[(y*9) + x])


def single_line_board(board):
    '''
    used to convert board object to just numbers in a str
    '''
    board_str = str(board)
    board_str = board_str.replace('0', '#')
    board_str = board_str.replace(' ', '')
    board_str = board_str.replace('\n', '')
    return board_str


def display_board(board, single_line=True):
    '''
    displays the board to user in a more friendly manor

    args:
        board (str or object): pass in str or the board object itself
        single_line (bool): set to false if passing in str version of board that is already stripped otherwise leave alone
    '''
    if single_line == True:
        board = single_line_board(board)

    B = list(board)
    def I():
        C = B[0]
        del B[0]
        return str(C)
    
    print(
        ' ——————————————————— \n'
        f'|{I()}|{I()}|{I()}||{I()}|{I()}|{I()}||{I()}|{I()}|{I()}|\n'
        f'|{I()}|{I()}|{I()}||{I()}|{I()}|{I()}||{I()}|{I()}|{I()}|\n'
        f'|{I()}|{I()}|{I()}||{I()}|{I()}|{I()}||{I()}|{I()}|{I()}|\n'
        '|—————||—————||—————|\n'
        f'|{I()}|{I()}|{I()}||{I()}|{I()}|{I()}||{I()}|{I()}|{I()}|\n'
        f'|{I()}|{I()}|{I()}||{I()}|{I()}|{I()}||{I()}|{I()}|{I()}|\n'
        f'|{I()}|{I()}|{I()}||{I()}|{I()}|{I()}||{I()}|{I()}|{I()}|\n'
        '|—————||—————||—————|\n'
        f'|{I()}|{I()}|{I()}||{I()}|{I()}|{I()}||{I()}|{I()}|{I()}|\n'
        f'|{I()}|{I()}|{I()}||{I()}|{I()}|{I()}||{I()}|{I()}|{I()}|\n'
        f'|{I()}|{I()}|{I()}||{I()}|{I()}|{I()}||{I()}|{I()}|{I()}|\n'
        ' ——————————————————— '
        )

def board_filled(board):
    for x in range(9):
        for y in range(9):
            if board.get(x, y) == '.':
                return False
    return True


def game(board, original_board):
    mistakes = 0
    # solve board loop
    while True:
        system('cls')
        display_board(board)

        # grab user input loop
        while True:
            if 'restart' not in locals() or restart == True:
                restart = False
                system('cls')
                display_board(board)
            # grab Column cord
            while True:
                try:
                    user_input = int(input("Enter Column: "))
                except TypeError:
                    wrong_input('Please enter a Column (1-9), not text', board=board)
                else:
                    if user_input in range(1, 10):
                        x = user_input - 1
                        break
                    else:
                        wrong_input('Please enter a Column (1-9)', board=board)
                        
            # grab Row cord
            while restart == False:
                try:
                    user_input = int(input('Enter Row (Or "10" to restart process): '))
                except TypeError:
                    wrong_input('Please enter a row (1-9) or 10, not letters', board=board)
                else:
                    if user_input in range(1, 10):
                        y = user_input - 1
                        break
                    elif user_input == 10:
                        restart = True
                    else:
                        wrong_input('Please enter a row (1-9) or 10', board=board)

            # grab number for cell            
            while restart == False:
                try:
                    user_input = int(input('Enter Value for cell (Or "10" to restart process): '))
                except TypeError:
                    wrong_input('Please enter a number (1-9) or 10, not letters', board=board)
                else:
                    if user_input in range(1, 10):
                        number = user_input
                        break
                    elif user_input == 10:
                        restart = True
                    else:
                        wrong_input("Please enter a value (1-9) or 10", board=board)

            # user satisfied with setting cell to certain value
            if restart == False:
                break
        # end of grab user input loop
        

        if original_board.get(x, y) == number:
            board.set(x, y, number)
            if board_filled(board) == True:
                break
        else:
            mistakes += 1
            wrong_input(f"Wrong answer... You have {mistakes} mistakes.", board=board)
    # end of solve board loop
    system("cls")
    display_board(board)
    print(f"You Solved it! You had {mistakes} mistakes!")
    sleep(5)
    
            
    

def main():
    system('cls')
    print("Welcome to Sudoku!")

    while True:
        # user decides difficulty
        while True:
            try:
                user_input = int(input("What difficulty would you like? (1: for Easy 2: for Medium 3: for Hard.): "))
            except TypeError:
                wrong_input("Please enter a number (1-3) not text")
            else:
                if user_input in range(1, 4):
                    difficulty = user_input
                    break
                else:
                    wrong_input("Please enter a number (1-3)")

        # create board
        original_board_array, difficult_board_array = interact_with_C.create_board(difficulty)
        original_board = grid.Grid(9, 9)
        difficult_board = grid.Grid(9, 9)
        convert_single_line_board(original_board, original_board_array)
        convert_single_line_board(difficult_board, difficult_board_array)
        game(difficult_board, original_board)

        while True:
            system('cls')
            user_input = input("Would you like to play again? (Y/N): ")
            user_input.lower()
            if user_input == 'n':
                break
            elif user_input == 'y':
                return
            else:
                wrong_input("Please enter a valid answer (Y/N)")




if __name__ == "__main__":
    main()
