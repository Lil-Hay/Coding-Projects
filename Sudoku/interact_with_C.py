import ctypes
import os

def create_board(difficulty):
    write_board = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "Sudoku_Board.dll"))
    write_board.create_board_python.argtypes = None
    write_board.create_board_python.restype = ctypes.POINTER(ctypes.c_int)

    c_filled_board_array_ptr = write_board.create_board_python()
    filled_board_array = ctypes.cast(c_filled_board_array_ptr, ctypes.POINTER(ctypes.c_int * 81)).contents


    write_board.create_difficulty_python.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    write_board.create_difficulty_python.restype = ctypes.POINTER(ctypes.c_int)
    c_difficult_board_array_ptr = write_board.create_difficulty_python(c_filled_board_array_ptr, difficulty)
    difficult_board_array = ctypes.cast(c_difficult_board_array_ptr, ctypes.POINTER(ctypes.c_int * 81)).contents

    filled_board = []
    for i in range(81):
        filled_board.append(filled_board_array[i])


    difficult_board = []
    for i in range(81):
        difficult_board.append(difficult_board_array[i])

    return filled_board, difficult_board

if __name__ == "__main__":
    create_board(3)
