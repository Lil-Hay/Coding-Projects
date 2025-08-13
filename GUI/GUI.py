import tkinter as tk

def create_board():
    import grid
    import os
    board = grid.Grid(9, 9)
    filled_board = grid.Grid(9, 9)

    with open((os.path.join(os.path.dirname(__file__),"Board.txt"))) as f:
            Board_single_line = f.readline()
            filled_board_single_line = f.readline()
    Board_list = list(Board_single_line)
    filled_board_list = list(filled_board_single_line)
    for x in range(9):
            for y in range(9):
                    board.set(x, y, Board_list[(y*9) + x])
    for x in range(9):
            for y in range(9):
                    filled_board.set(x, y, filled_board_list[(y*9) + x])


    print(board)
    print(filled_board)

    return board, filled_board



def game(board, filled_board):
    global root
    root = tk.Tk()
    root.title("Sudoku")
    global mistake_count, second, minute, game_frame

    mistake_count = 0
    second = 0
    minute = 0

    game_frame = tk.Frame(root)
    game_frame.pack()
    info_frame = tk.Frame(game_frame)
    info_frame.pack(side="top", padx=10, pady=10)

    mistakes = tk.Label(info_frame, text=(f"Mistakes: {mistake_count}"), font=("Arial", 16), justify="right")
    mistakes.pack(side="right", padx=10, anchor="e")

    timer = tk.Label(info_frame, text="Time: 0 Minutes: 0 Seconds" , font=("Arial", 16), justify= "left")
    timer.pack(side="left", padx=10, anchor="w")

    sudoku_frame = tk.Frame(game_frame, bg="black", bd=2) # bd for border around the whole grid
    sudoku_frame.pack(side="bottom", padx=10, pady=10)
                
    blocks = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            blocks[i][j] = tk.Frame(sudoku_frame, bd=3, relief="ridge", bg="lightgray")
            blocks[i][j].grid(row=i, column=j, padx=2, pady=2, sticky="nsew")

    cells = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            # Determine which 3x3 block the cell belongs to
            block_row = i // 3
            block_col = j // 3
            if board.get(j, i) == '0':
                # Create an Entry widget for the cell
                cell_entry = tk.Entry(blocks[block_row][block_col], width=4, font=("Arial", 16),
                                        justify="center", relief="solid", bd=1)
                                
                # Place the cell within its respective 3x3 block
                cell_entry.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                
                cell_entry.bind("<Return>", lambda event, i=i, j=j: get_user_input(i, j))
                cells[i][j] = cell_entry
            else:
                # Create a Label widget for the cell
                cell_label = tk.Label(blocks[block_row][block_col], text=str(board.get(j, i)), width=4, font=("Arial", 16),
                                        justify="center", relief="solid", bd=1)
                # Place the cell within its respective 3x3 block
                cell_label.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                cells[i][j] = cell_label

    def get_user_input(i, j):
        user_value = cells[i][j].get().strip()
        # Do something with the user values
        if user_value == filled_board.get(j, i):
            # Destroy the entry widget
            cells[i][j].destroy()
            # Determine which 3x3 block the cell belongs to
            block_row = i // 3
            block_col = j // 3
            # Create a new label widget with the same value
            cell_label = tk.Label(blocks[block_row][block_col], text=user_value, width=4, font=("Arial", 16), justify="center", relief="solid", bd=1)
            cell_label.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
            # Update the cells array to point to the new label widget
            cells[i][j] = cell_label
            if check_board_filled() == True:
                return_to_main()
        else:
            cells[i][j].config(bg="red")
            global mistake_count
            mistake_count += 1
            mistakes.config(text=(f"Mistakes: {mistake_count}"))

    def check_board_filled():
        for i in range(9):
            for j in range(9):
                if cells[i][j] == cell_entry:
                    return False
        return True

    def update_time():
        global minute, second
        second += 1
        if second == 60:
            second = 0
            minute += 1
        time = f"{minute} Minutes: {second} Seconds"
        timer.config(text=f"Time: {time}")
        root.after(1000, update_time)



    update_time()

    def transition_to_new_game_menu():
        # Remove the current game screen
        game_frame.pack_forget()
        # Create the new game menu screen
        global new_game_menu_frame
        new_game_menu_frame = tk.Frame(root)
        new_game_menu_frame.pack(fill="both", expand=True)

        # Add widgets to the new game menu screen
        new_game_menu_label = tk.Label(new_game_menu_frame, text="New Game Menu")
        new_game_menu_label.pack()

        # Add a button to start a new game
        start_new_game_button = tk.Button(new_game_menu_frame, text="Start New Game", command=lambda: game(board, filled_board))
        start_new_game_button.pack()

        # Add a button to quit the game
        quit_game_button = tk.Button(new_game_menu_frame, text="Quit Game", command=root.destroy)
        quit_game_button.pack()


def transition_to_game():
    # Remove the current main menu screen
    global root
    root.destroy()
    # Create the game screen
    board, filled_board = create_board()
    # call game and delete this part of call stack
    game(board, filled_board)

def return_to_main():
    # Remove the current game screen
    global root
    root.destroy()
    main()

    


def main():
    global root, main_menu_frame
    root = tk.Tk()
    root.title("Sudoku")

    main_menu_frame = tk.Frame(root)
    main_menu_frame.pack(fill="both", expand=True)

    main_menu_label = tk.Label(main_menu_frame, text="Main Menu")
    main_menu_label.pack()

    start_game_button = tk.Button(main_menu_frame, text="Start Game", command=lambda: transition_to_game())
    start_game_button.pack()

    quit_game_button = tk.Button(main_menu_frame, text="Quit Game", command=root.destroy)
    quit_game_button.pack()

    root.mainloop()



if __name__ == "__main__":
    main()