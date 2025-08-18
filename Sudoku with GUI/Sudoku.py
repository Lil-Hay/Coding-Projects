import tkinter as tk
from tkinter import ttk
#import os

def create_board(difficulty=str):
    import grid
    
    match difficulty:
        case "Easy":
            difficulty = int(1)
        case "Medium":
            difficulty = int(2)
        case "Hard":
            difficulty = int(3)
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
    
    empty_cells = 0
    for x in range(9):
        for y in range(9):
            if board.get(x, y) == "0":
                empty_cells += 1

    print(empty_cells)
    print(board)
    print(filled_board)
    """
    return board, filled_board






def game(board, filled_board):

    global mistake_count, second, minute, root, game_frame, paused
    
    paused = False
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

    def validate_input(P):
        return P in '123456789'
    vcmd = root.register(validate_input)

    cells = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            # Determine which 3x3 block the cell belongs to
            block_row = i // 3
            block_col = j // 3
            if board.get(j, i) == "0":
                # Create an Entry widget for the cell
                cell_entry = tk.Entry(blocks[block_row][block_col], width=4, font=("Arial", 16),
                                        justify="center", relief="solid", bd=1, validate="key", validatecommand=(vcmd, "%P"))
                                
                # Place the cell within its respective 3x3 block
                cell_entry.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                
                cell_entry.bind("<Key>", lambda event, i=i, j=j: get_user_input(i, j))
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
        if paused == True:
            cells[i][j].delete(0, tk.END)
            return
        if len(user_value) != 1:
            cells[i][j].delete(0, tk.END)
            return
        try:
            user_value = int(user_value)
        except ValueError:
            cells[i][j].delete(0, tk.END)
            return
        if user_value == 0:
            cells[i][j].delete(0, tk.END)
            return
        def set_all_white():
            for i in range(9):
                for j in range(9):
                    if isinstance(cells[i][j], tk.Entry):
                        cells[i][j].config(bg="white")
        set_all_white()
        # Do something with the user values
        if user_value == int(filled_board.get(j, i)):
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
                new_game_menu()
        else:
            cells[i][j].config(bg="red")
            global mistake_count
            mistake_count += 1
            mistakes.config(text=(f"Mistakes: {mistake_count}"))

    def check_board_filled():
        for i in range(9):
            for j in range(9):
                if isinstance(cells[i][j], tk.Entry):
                    return False
        return True

    def update_time():
        global minute, second, update_time_id
        second += 1
        if second == 60:
            second = 0
            minute += 1
        time = f"{minute} Minutes: {second} Seconds"
        timer.config(text=f"Time: {time}")
        update_time_id = root.after(1000, update_time)

    def pause_game():
        global paused, paused_frame
        if paused == False:
            root.after_cancel(update_time_id)
            paused = True
            for i in range(9):
                for j in range(9):
                    if isinstance(cells[i][j], tk.Entry):
                        cells[i][j].config(state="disabled")
            paused_frame = tk.Frame(root, bg="black", bd=2) # bd for border around the whole grid
            paused_frame.place(x=0, y=0, relwidth=1, relheight=1)
            paused_label = tk.Label(paused_frame, text="Game Paused", font=("Arial", 24), bg="black", fg="white")
            paused_label.pack(pady=10, padx=10)
            paused_frame.tkraise()
        elif paused == True:
            paused_frame.destroy()
            update_time()
            for i in range(9):
                for j in range(9):
                    if isinstance(cells[i][j], tk.Entry):
                        cells[i][j].config(state="normal")
            paused = False    
        
    root.bind("p", lambda event: pause_game())
    update_time()



def new_game_menu():
    global game_frame, new_game_menu_frame, minute, second, mistake_count, update_time_id
    root.after_cancel(update_time_id)
    game_frame.destroy()
    difficulty = "Easy"
    def set_difficulty():
        nonlocal difficulty
        difficulty = difficulty_combobox.get()
    
    score = 100000
    score -= ((minute * 60) * 100) + (second * 100)
    score -= (mistake_count * 500)
    if score < 0:
        score = 0
    new_game_menu_frame = tk.Frame(root)
    new_game_menu_frame.pack()

    score_label = tk.Label(new_game_menu_frame, text=(f"Your final score is {score:,} points"), font=("Arial", 24))
    score_label.pack(pady=10, padx=10)

    time_label = tk.Label(new_game_menu_frame, text=(f"You finished in {minute} minutes and {second} seconds"))
    time_label.pack(pady=10)

    mistakes_label = tk.Label(new_game_menu_frame, text=(f"You made {mistake_count} mistakes"))
    mistakes_label.pack(pady=10)

    difficulty_combobox = ttk.Combobox(new_game_menu_frame, values=["Easy", "Medium", "Hard"])
    difficulty_combobox.set("Easy")
    difficulty_combobox.bind("<<ComboboxSelected>>", lambda event: set_difficulty())
    difficulty_combobox.pack(pady=10)
    
    start_game_button = tk.Button(new_game_menu_frame, text="Start Game", command=lambda: transition_to_newgame(difficulty))
    start_game_button.pack(pady=10)

    quit_game_button = tk.Button(new_game_menu_frame, text="Quit Game", command=lambda: root.destroy())
    quit_game_button.pack(pady=10)
    


def transition_to_newgame(difficulty=str):
    global new_game_menu_frame
    new_game_menu_frame.destroy()
    loading_frame = tk.Frame(root)
    loading_frame.pack()
    loading_label = tk.Label(loading_frame, text="Loading...", font=("Arial", 32))
    loading_label.pack(pady=10, padx=10)

    # Update the GUI to display the loading screen
    root.update_idletasks()

    # Call create_board in a separate thread
    def create_board_and_start_game():
        board, filled_board = create_board(difficulty)
        loading_frame.destroy()
        game(board, filled_board)

    root.after(0, create_board_and_start_game)
     
def transition_to_game(difficulty=str):
    global main_menu_frame
    main_menu_frame.destroy()
    loading_frame = tk.Frame(root)
    loading_frame.pack()
    loading_label = tk.Label(loading_frame, text="Loading...", font=("Arial", 32))
    loading_label.pack(pady=10, padx=10)

    # Update the GUI to display the loading screen
    root.update_idletasks()

    # Call create_board in a separate thread
    def create_board_and_start_game():
        board, filled_board = create_board(difficulty)
        loading_frame.destroy()
        game(board, filled_board)

    root.after(0, create_board_and_start_game)



def main_menu():
    global root, main_menu_frame
    difficulty = "Easy"
    def set_difficulty():
        nonlocal difficulty
        difficulty = difficulty_combobox.get()
    
    main_menu_frame = tk.Frame(root)
    main_menu_frame.pack()

    title_label = tk.Label(main_menu_frame, text="Sudoku", font=("Arial", 24))
    title_label.pack(pady=10)

    difficulty_combobox = ttk.Combobox(main_menu_frame, values=["Easy", "Medium", "Hard"])
    difficulty_combobox.set("Easy")
    difficulty_combobox.bind("<<ComboboxSelected>>", lambda event: set_difficulty())
    difficulty_combobox.pack(pady=10, padx=10)

    start_button = tk.Button(main_menu_frame, text="Start Game", command=lambda: transition_to_game(difficulty))
    start_button.pack(pady=10)

    quit_game_button = tk.Button(main_menu_frame, text="Quit Game", command=lambda: root.destroy())
    quit_game_button.pack(pady=10)
    




if __name__ == "__main__": 
    root = tk.Tk()
    root.title("Sudoku Game")
    global mistake_count, second, minute
    main_menu()
    root.mainloop()
