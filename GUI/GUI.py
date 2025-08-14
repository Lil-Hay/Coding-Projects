import tkinter as tk
from tkinter import ttk

def create_board(difficulty=str):
    import grid
    match difficulty:
        case "Easy":
            difficulty = 1
        case "Medium":
            difficulty = 2
        case "Hard":
            difficulty = 3
    def convert_single_line_board(grid, board):
        for x in range(9):
            for y in range(9):
                grid.set(x, y, str(board[(y*9) + x]))
    board = grid.Grid(9, 9)
    filled_board = grid.Grid(9, 9)
    import interact_with_C
    filled_board_str, board_str  = interact_with_C.create_board(difficulty)
    convert_single_line_board(board, board_str)
    convert_single_line_board(filled_board, filled_board_str)
    
    

    """
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
    """

    print(board)
    print(filled_board)

    return board, filled_board



def game(board, filled_board):
    global root, new_game
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
            if board.get(j, i) == "0":
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
                global new_game
                new_game = 1
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
        global minute, second, new_game
        if new_game == 1:
            root.destroy()
            global return_value
            return_value = 2
            return
        second += 1
        if second == 60:
            second = 0
            minute += 1
        time = f"{minute} Minutes: {second} Seconds"
        timer.config(text=f"Time: {time}")
        root.after(1000, update_time)
    

    update_time()

    root.mainloop()


def transition_to_game():
    # Remove the current main menu screen
    global root, return_value
    root.destroy()
    # call game and delete this part of call stack
    return_value = 1

def exit():
    global root, return_value
    return_value = 0
    root.destroy()




def main_menu():
    global root, main_menu_frame, difficulty
    root = tk.Tk()
    root.title("Sudoku")
    def set_difficulty(event):
        global difficulty
        difficulty = event.widget.get()
    main_menu_frame = tk.Frame(root)
    main_menu_frame.pack(fill="both", expand=True)

    main_menu_label = tk.Label(main_menu_frame, text="Main Menu")
    main_menu_label.pack()

    difficulty_combobox = ttk.Combobox(main_menu_frame, values=["Easy", "Medium", "Hard"])
    difficulty_combobox.set("Easy")
    difficulty_combobox.bind("<<ComboboxSelected>>", set_difficulty)
    difficulty_combobox.pack()

    start_game_button = tk.Button(main_menu_frame, text="Start Game", command=lambda: transition_to_game())
    start_game_button.pack()

    quit_game_button = tk.Button(main_menu_frame, text="Quit Game", command=root.destroy)
    quit_game_button.pack()

    root.mainloop()

def transition_to_new_game():
    global return_value
    global root, new_gameframe
    root = tk.Tk()
    root.title("Sudoku")

    new_gameframe = tk.Frame(root)
    new_gameframe.pack(fill="both", expand=True)

    new_game_label = tk.Label(new_gameframe, text="New Game")
    new_game_label.pack()
    
    stats_label = tk.Label(new_gameframe, text=(f"Stats: Finished in {minute} minutes and {second} seconds with {mistake_count} mistakes"))
    stats_label.pack()

    start_game_button = tk.Button(new_gameframe, text="Start Game", command=lambda: transition_to_game())
    start_game_button.pack()

    quit_game_button = tk.Button(new_gameframe, text="Quit Game", command=lambda: exit())
    quit_game_button.pack()

    root.mainloop()


def main():
    global return_value, new_game, difficulty
    difficulty = "Easy"
    return_value = 0
    main_menu()
    while True:
        print(difficulty)
        new_game = 0
        if return_value == 2:
            transition_to_new_game()
        elif return_value == 1:
            board, filled_board = create_board(difficulty)
            game(board, filled_board)
        elif return_value == 0:
                    break


if __name__ == "__main__":
    main()