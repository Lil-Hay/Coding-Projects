class piece:
    def __init__(self, color):
        self.color = color + " piece"
        self.flipped = False
    def get_color(self):
        return self.color
    def get_flipped(self):
        return self.flipped
    
class cell:
    def __init__(self, color, object=None):
        if color == "red":
            self.color = "red cell"
        if color == "black":
            self.color = "black cell"
            self.piece = object
    def get_cell_color(self):
        return self.color
    def get_piece_color(self):
        if isinstance(self.piece, piece):
            return self.piece.get_color()
        return "empty"
    def get_piece_state(self):
        if isinstance(self.piece, piece):
            return self.piece.get_flipped()
        return "empty"
        

class Checkers_Board:
    def __init__(self):
        self.board = [[1 for _ in range(8)] for _ in range(8)]
        valid = False
        color = "black"
        for x in range(8):
            if x == 5:
                color = "red"
            for y in range(8):
                if 2 < x < 5:
                    if valid == True:
                        self.board[x][y] = cell("black")
                    else:
                        self.board[x][y] = cell("red")
                    if y != 7:
                        valid = not valid
                
                else:
                    if valid == True:
                        self.board[x][y] = cell("black", piece(color))
                    else:
                        self.board[x][y] = cell("red")
                    if y != 7:    
                        valid = not valid
    
    def get_value(self, x, y):
        _cell = self.board[x][y]
        if _cell.get_cell_color() == "red cell":
            return "red cell"
        else:
            return _cell.get_piece_color()
        
    def __str__(self):
        rows = []
        for x in range(8):
            for y in range(8):
                value = self.get_value(x,y)
                match value:
                    case "red piece":
                        value = "\033[31mO\033[0m"
                    case "red cell":
                        value = '\033[31mX\033[0m'
                    case 'empty':
                        value = "X"
                    case "black piece":
                        value = "O"
                rows.append(value + ' ')
            rows.append("\n")
        return ''.join(rows)
                
checkers_board = Checkers_Board()
print(checkers_board)