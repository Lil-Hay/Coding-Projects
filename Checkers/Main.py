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
    def get_piece_color(self, x, y):
        if self.board[x][y].get_piece_color() == "empty":
            return "empty"
        return self.board[x][y].get_piece_color()
    
    def get_piece_state(self, x, y):
        if self.board[x][y].get_piece_color() == "empty":
            return "empty"
        return self.board[x][y].get_piece_state()
    
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

def move_backwards(checkers_board, move):
    if move["move_x"] > move["move_to_x"]:
        return False

    if checkers_board.get_piece_state(move["move_x"], move["move_y"]) == False:
        return False


def is_move_valid(checkers_board, move):
    if checkers_board.get_value(move["move_x"], move["move_y"]) != "red piece":
        return False
    if checkers_board.get_value(move["move_to_x"], move["move_to_y"]) != "empty":
        return False
    if move_backwards(checkers_board,move):
        print("move backwards")
        return
    print("expected")


def create_move(checkers_board):
    print(checkers_board)
    print("what is the piece you'd like to move?")
    move_x = int(input("enter x cord: "))
    move_y = int(input("enter y cord: "))
    move_to_x = int(input("enter x cord: "))
    move_to_y = int(input("enter y cord: "))
    return {"move_x": move_x, "move_y": move_y, "move_to_x": move_to_x, "move_to_y": move_to_y}

if __name__ == "__main__":
    checkers_board = Checkers_Board()
    move = create_move(checkers_board)
    is_move_valid(checkers_board, move)
    

    print(checkers_board)