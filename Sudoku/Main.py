import Create_Difficulty
import Create_Board
from os import system
from time import sleep
import copy

board = "8 9 2 6 3 4 1 5 7\n7 5 4 2 1 9 8 3 6\n3 1 6 8 5 7 9 2 4\n6 2 1 3 8 5 4 7 9\n4 3 8 9 7 1 5 6 2\n5 7 9 4 2 6 3 8 1\n1 8 3 7 9 2 6 4 5\n2 4 5 1 6 8 7 9 3\n9 6 7 5 4 3 2 1 8"
def single_line_board(board):
    '''
    used to convert board object to just numbers in a str
    '''
    board_str = str(board)
    board_str = board_str.replace('.', '#')
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

            
    

def main():
    system('cls')
    print("Welcome to Sudoku!")

    # grab user input
    while True:
        try:
            user_input = int(input("What diffuculty would you like? (1: for Easy 2: for Medium 3: for Hard.): "))
        except TypeError:
            print("Please enter a number (1-3) not text")
        else:
            if user_input in range(1, 4):
                difficulty = user_input
                break
            else:
                print("Please enter a number (1-3)")

    # create valid boards
    board = Create_Board.create_board()
    orginal_board = copy.deepcopy(board)
    display_board(board)

    # create puzzle
    board = Create_Difficulty.create_difficulty(board, difficulty)
    display_board(board)







        







if __name__ == "__main__":
    main()
