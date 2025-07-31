import struct
import socket
from time import sleep as wait
from random import randrange
from grid import Grid as grid
import Files
def check_client(client):
    global Client_1, Client_2
    if client == Client_1:
        return 1
    if client == Client_2:
        return 2

def close_both():
    global Client_1, Client_2, closed, Client_1_Nick, Client_2_Nick
    
    if closed != True:
        closed = True

        if send("Other player lost connection... waiting for another player.", Client_1, "12") == False: 
            print("Client 1 disconnected") # Client 1 disconnects
            Client_1, Client_1_Nick = None, None
            if send("Other player lost connection... waiting for another player.", Client_2, "12") == False: 
                print("Client 2 disconnected") # client 1 is still here but client 2 is not
                Client_2, Client_2_Nick = None, None
                return
        else: 
            if send("Other player lost connection... waiting for another player.", Client_2, "12") == False: 
                print("Client 2 disconnected") # client 1 is still here but client 2 is not
                Client_2, Client_2_Nick = None, None
                return
            else: 
                return # both clients are still here




def create_socket(clients=1, production=False):
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket object
    try:            
        # bind ip (first arg) and port (second arg) to socket.
        # IP should be '0.0.0.0' for production.
        # Local host is socket.gethostbyname(socket.gethostname())
        if production == True:
            Socket.bind(('0.0.0.0', 9090))
        else:
            Socket.bind((socket.gethostbyname(socket.gethostname()), 9090))
            print("NOT PRODUCTION")
    except:
        print("handled bind exception") 
    else:
        Socket.listen(clients) # allows for one connection at time and listens for connections
        return Socket 


def send(message='', Client=False, command=None):
    """
        Sends message to client or clients.

        Args:
            message: enter message to send.
            Client: pass client object to send to or pass False to send to both objects.
            command: "1" tells client to clear screen, "2" tells client to expect consecutive messages, "3" specifies to expect str. add any combination to execute, "4" tells client to disconnect.
        """
    global restart
    if command != None:
        if command.find('1') != -1:
            message += 'CLEAR_SCREEN'

        if command.find('2') != -1:
            message += 'SECOND_MESSAGE'

        if command.find('3') != -1:
            message += 'TYPE=STR'

        if command.find('4') != -1:
            message += 'DISCONNECT'

    
    
    if Client == False:
        try:
            Client_1.send(message.encode('utf-8'))

        except:
            print("Connection Failed on send to both clients, Client 1")
            restart = True
            close_both()
            return False
        
        try:
            Client_2.send(message.encode('utf-8'))

        except:
            print("Connection Failed on send to both clients, Client 2")
            restart = True
            close_both()
            return False
    else:        
        try: # try catch so server doesn't crash with unhandled exception
            Client.send(message.encode('utf-8'))
        except:
            print(f"Connection Failed on send to client {check_client(Client)}")
            restart = True
            close_both()
            return False


def receive(client, type=int):
    """
        Receive message from client.

        Args:
            client: Pass client object to receive message from
            type: By default expects int, pass "str" instead if you need to receive a string
        """
    global restart
    if type == int:
        try: # try catch to prevent server from crashing due to unhandled exception
            encoded_transmission = client.recv(4) # receive data from client
            decoded_transmission = struct.unpack('!i', encoded_transmission)[0] # decode int from client
            return int(decoded_transmission) # return back int to use with other fuctions
    
        except: #handle exception
            print(f"Connection Failed on receive int from Client {check_client(client)}")
            close_both()
            restart = True
            return False
            
    if type == str:
        try:
            data = client.recv(1024).decode('utf-8')
            if data == "":
                return False
            if data != None:
                return data
            
        except:
            print(f"Connection Falied on receive str from Client {check_client(client)}")
            close_both()
            restart = True
            return
        
def invalid_choice(client, message="Please enter a valid number (1-3)", print_board=True):
    send(message, client, '12')
    wait(1.5)
    if print_board == True:
        send(board_str(), client, '12')

        
def grab_input(client):
    
    if client == Client_1:
        mark = "X"
    elif client == Client_2:
        mark = "O"
    else:
        print("Issue with assigning mark to player")

    while True:
        if restart == True:
            return
        go_back = False
        while True:
            if restart == True:
                return
            try:
                send('Please enter column to play (1-3) ', client)
                x = receive(client) - 1
                if x > -1 and x < 3:
                    break
                else:
                    invalid_choice(client)
            except:
                invalid_choice(client)
        while True:
            if restart == True:
                return
            try:
                send("Please enter row to play (1-3) or 4 to go back: ", client)
                y = receive(client) - 1    
                if y > -1 and y < 3:
                    break
                elif y == 3:
                    go_back = True
                    send(board, client, '12')
                    break
                else:
                    invalid_choice(client, "Please enter a valid number (1-4)") 
                    go_back = True
                    break
            except:
                invalid_choice(client, "Please enter a valid number (1-4)")
                go_back = True
                break
        if go_back != True:        
            if board.get(x, y) == ".":
                board.set(x, y, mark)
                return
            else:
                invalid_choice(client, "Already used, try again")

def board_str():
    return str(board)



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



def winner():
    winner = check_winner()
    match winner:
        case 'X': # Client 1 wins
            send(board_str(), False, '12')
            send("You Won!", Client_1, '2')
            send("You Lost", Client_2, '2')
            Files.write_stats(Client_2_Nick, "L")
            Files.write_stats(Client_1_Nick, "W")
        case 'O': # Client 2 wins
            send(board_str(), False, '12')
            send("You Won!", Client_2, '2')
            send("You Lost", Client_1, '2')
            Files.write_stats(Client_1_Nick, "L")
            Files.write_stats(Client_2_Nick, "W")
        case _:
            return
    return True



def game():
    if "board" not in globals():
        global board
    board = grid(3, 3, ".")
    turns = 1

    global Client_1_First
    if Client_1_First == True:
        while True:
            if restart == True:
                return
            

            # First player turn
            send(board_str(), False, '12')
            send("Waiting on other player.", Client_2, '2')
            grab_input(Client_1)
            if turns > 2:
                if winner() == True:
                    return
                
            if turns == 5: # tie scenerio
                break

            if restart == True:
                return

            # second player turn
            send(board_str(), False, '12')
            send("Waiting on other player.", Client_1, '2')
            grab_input(Client_2)
            if turns > 2:
                if winner() == True:
                    return
            turns += 1

    elif Client_1_First == False:
        while True:
            if restart == True:
                return
            
            # second player turn
            send(board_str(), False, '12')
            send("Waiting on other player.", Client_1, '2')
            grab_input(Client_2)
            if turns > 2:
                if winner() == True:
                    return
                
            if turns == 5: # tie scenerio
                break

            if restart == True:
                return


            # first player turn
            send(board_str(), False, '12')
            send("Waiting on other player.", Client_2, '2')
            grab_input(Client_1)
            if turns > 2:
                if winner() == True:
                    return
            
            turns += 1
    

    # Game Ties
    send(board_str()+ '\nGame Tied!', False, '12')
    Files.write_stats(Client_1, "T")
    Files.write_stats(Client_2, "T")
    return
        

def send_stats():
    global Client_1_Nick, Client_2_Nick
    Client_1_Stats = Files.read_stats(Client_1_Nick)
    Client_2_Stats = Files.read_stats(Client_2_Nick)
    send(f'"{Client_1_Nick}" has {Client_1_Stats["W"]} Wins, {Client_1_Stats["L"]} Losses, and {Client_1_Stats["T"]} Ties!'
         + f'\n"{Client_2_Nick}" has {Client_2_Stats["W"]} Wins, {Client_2_Stats["L"]} Losses, and {Client_2_Stats["T"]} Ties!',
        False, "2")
    return



def game_main():

    if restart != True:
        send("Welcome to Tik Tak Toe!", False, '12')


    while True:
        if restart == True:
            return
    
        if "Client_1_First" not in globals():
            global Client_1_First
            Client_1_First = False

        wait(0.5)

        send_stats()

        wait(3)
        
        game()

        Client_1_First = not Client_1_First


    
def grab_user(Client):
    send("Enter your Nickname:", Client, "13")

    
    if Client==Client_1:
        global Client_1_Nick
        Client_1_Nick = receive(Client, str)
        username = Client_1_Nick
    elif Client==Client_2:
        global Client_2_Nick
        Client_2_Nick = receive(Client, str)
        username = Client_2_Nick


    tries = 0
    while tries < 5:
        send("Enter your password:", Client, "13")
        if Files.Password_Correct(username, receive(Client, str)) == True:
            return
        send("Wrong Password, Try again", Client, '12')
        wait(1.5)
        tries += 1
    
    send("Too many failed attempts\nIf you'd like to change your password, contact Server Admin", Client, "14")
    try:
        Client.close()
    except:
        pass
    return
    





def main():
    global restart
    global Server
    global closed
    Server = create_socket(2, True)
    global Client_1, Client_2
    Client_1, Client_2 = None, None
    while True:
        closed = False
        restart = False

        # getting ready for players
        if Client_1 is None:
            if Client_2 != None:
                wait(0.5)
                send("Other player disconnected, Waiting for Second Player", Client_2, "12")
            Client_1, addr1 = Server.accept()
            print(f"Connected to first client {addr1}")
            grab_user(Client_1)
            send("Waiting for Second Player", Client_1, "12")
        else:
            wait(0.5)
            send("Other player disconnected, Waiting for Second Player", Client_1, "12")

        if restart == False and Client_1 != None and Client_2 is None:
                Client_2, addr2 = Server.accept()
                print(f"Connected to second client {addr2}")
                grab_user(Client_2)

        if restart == False:
            game_main()

    


        







if __name__ == '__main__':
    print("Start of server program")
    main()