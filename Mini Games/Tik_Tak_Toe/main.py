from .grid import Grid as grid
from random import randint
from os import system
from time import sleep
import Main_Menu

def display_stats(stats):
    stats = stats
    clear(0)
    print(f'You have: \n{stats[0]} Wins \n{stats[1]} Losses \n{stats[2]} Ties')
    clear(3)

def clear(pause=1.5):
    sleep(pause)
    system("cls")

def invaid_choice(message="Please enter a valid number (1-3)", print_board=True):
    clear(0)
    print(message)
    clear(1.5)
    if print_board == True:
        print(board)

def grab_input():
    
    while True:
        go_back = False
        while True:
            try:
                x = int(input("Please enter column to play (1-3): ")) - 1
                if x > -1 and x < 3:
                    break
                else:
                    invaid_choice()
            except:
                invaid_choice()
        while True:
            try:
                y = int(input("Please enter row to play (1-3) or 4 to go back: ")) - 1    
                if y > -1 and y < 3:
                    break
                elif y == 3:
                    go_back = True
                    clear(0)
                    print(board)
                    break
                else:
                    invaid_choice()
                    go_back = True
                    break
            except:
                invaid_choice()
                go_back = True
                break
        if go_back != True:        
            if board.get(x, y) == ".":
                board.set(x, y, "X")
                return
            else:
                invaid_choice("Already used, try again")

def ai_choice():
    # Try to win
    for x in range(3):
        for y in range(3):
            if board.get(x, y) == ".":
                board.set(x, y, "O")
                if check_winner() == "O":
                    return
                board.set(x, y, ".")
    # Block player
    for x in range(3):
        for y in range(3):
            if board.get(x, y) == ".":
                board.set(x, y, "X")
                if check_winner() == "X":
                    board.set(x, y, "O")
                    return
                board.set(x, y, ".")
    # Otherwise, random
    while True:
        x = randint(0, 2)
        y = randint(0, 2)
        if board.get(x, y) == ".":
            board.set(x, y, "O")
            return

def board_filled():
    x = 0
    y = 0
    for i in range(3):
        for i in range(3):
            if board.get(x, y) == ".":
                return False
            y += 1
        y = 0
        x += 1
    return True

def winner():
    winner = check_winner()
    match winner:
        case 'X':
            Stats[0] += 1
            clear(0)
            print(board)
            print("YOU WON!")
            return True
        case 'O':
            Stats[1] += 1
            clear(0)
            print(board)
            print("YOU LOST")
            return True
        case _:
            return
        


def check_winner():
    # Check rows and columns
    for i in range(3):
        # Rows
        if board.get(0, i) == board.get(1, i) == board.get(2, i) != ".":
            return board.get(0, i)
        # Columns
        if board.get(i, 0) == board.get(i, 1) == board.get(i, 2) != ".":
            return board.get(i, 0)
    # Diagonals
    if board.get(0, 0) == board.get(1, 1) == board.get(2, 2) != ".":
        return board.get(0, 0)
    if board.get(2, 0) == board.get(1, 1) == board.get(0, 2) != ".":
        return board.get(2, 0)
    return None


def game():
    global board
    board = grid(3, 3, ".")
    turns = 1
    
    
    while True:
        clear(0)

        match player_first:
            case True:
                print(board)
                grab_input()
                if turns > 2:
                    if winner() == True:
                        return
                
                if turns == 5:
                    break
                
                ai_choice()
                if turns > 2:
                    if winner() == True:
                        return
            case False:
                ai_choice()
                if turns > 2:
                    if winner() == True:
                        return
                
                if turns == 5:
                    break
                
                print(board)
                grab_input()
                if turns > 2:
                    if winner() == True:
                        return

        turns += 1
    clear(0)
    Stats[2] += 1
    print(board)
    print("Game Over")
    
    

def main():
    global Stats
    Stats = [0, 0, 0] #[0] = Wins, [1] = losses, [2] = ties
    clear(0)
    print("Welcome to Tik Tak Toe!")
    clear()
    global player_first
    player_first = True
    game()


    while True:
        clear()
        try:
            user_input = int(input("Would you like to play again (1), Return to Main Menu (2), or Exit (3): "))
            match user_input:
                case 1:
                    player_first = not player_first
                    display_stats(Stats)
                    game()
                case 2:
                    played_once = Stats[0] + Stats[1] + Stats[2]
                    if played_once != 1:
                        display_stats(Stats)
                    Main_Menu.main()
                case 3:
                    played_once = Stats[0] + Stats[1] + Stats[2]
                    if played_once != 1:
                        display_stats(Stats)
                    return
                case _ :
                    invaid_choice("Please enter a valid answer (1-3)", False)
        except:
            invaid_choice("Please enter a valid answer (1-3)", False)


        



if __name__ == "__main__":
    main()
