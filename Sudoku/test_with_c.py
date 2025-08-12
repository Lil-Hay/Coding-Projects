import ctypes

write_board = ctypes.CDLL("C:/test/Sudoku_Board.so")
write_board.create_sudoku.argtypes = (ctypes.c_int)
write_board.create_sudoku(3)