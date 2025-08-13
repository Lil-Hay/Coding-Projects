from tkinter import *
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

import tkinter as tk
root = tk.Tk()
root.title("Sudoku Grid")

sudoku_frame = tk.Frame(root, bg="black", bd=2) # bd for border around the whole grid
sudoku_frame.pack(padx=10, pady=10)
              
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
    user_value = cells[i][j].get()
    # Do something with the user values
    if user_value == filled_board.get(j, i):
        cells[i][j].config(bg="green")
    else:
        cells[i][j].config(bg="red")


root.mainloop()