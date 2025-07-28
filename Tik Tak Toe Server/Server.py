import struct
import socket
from time import sleep as wait
from random import randrange
from grid import Grid as grid




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
    except:
        print("handled bind exception") 
    else:
        Socket.listen(clients) # allows for one connection at time and listens for connections
        return Socket 


def send(message='', Client=False, command=None):
    global restart
    """
        Sends message to client or clients.

        Args:
            message: enter message to send.
            Client: pass client object to send to or pass False to send to both objects.
            command: "1" tells client to clear screen, "2" tells client to expect consecutive messages, "3" specifies to expect str. add any combination to execute.
        """
    
    if command != None:
        if command.find('1') != -1:
            message += 'CLEAR_SCREEN'

        if command.find('2') != -1:
            message += 'SECOND_MESSAGE'

        if command.find('3') != -1:
            message += 'TYPE=STR'

    
    if Client == False:
        try:
            Client_1.send(message.encode('utf-8'))
            Client_2.send(message.encode('utf-8'))
        except:
            print("Connection failed on send")
            restart = True
            return
    else:        
        try: # try catch so server doesn't crash with unhandled exception
            Client.send(message.encode('utf-8'))
        except:
            print("Connection Lost on send")
            restart = True
            return


def receive(client, type=int):
    global restart
    """
        Receive message from client.

        Args:
            client: Pass client object to receive message from
            type: By default expects int, pass "str" instead if you need to receive a string
        """

    if type == int:
        try: # try catch to prevent server from crashing due to unhandled exception
            encoded_transmission = client.recv(4) # receive data from client
            decoded_transmission = struct.unpack('!i', encoded_transmission)[0] # decode int from client
            return int(decoded_transmission) # return back int to use with other fuctions
    
        except: #handle exception
            print("Connection Lost on receive")
            restart = True
            return
            
    if type == str:
        try:
            return client.recv(1024).decode('utf-8')
        except:
            print("Connection Lost on receive")
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
    else:
        mark = "O"

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

def game():
    
    if "board" not in globals():
        global board
    board = grid(3, 3, ".")
    turns = 1

    while True:

        if restart == True:
            return  

        match Client_1_First:
            case True:
                    send(board_str(), False, '12')
                    send("Waiting on other player.", Client_2, '2')
                    grab_input(Client_1)

                    send(board_str(), False, '12')
                    send("Waiting on other player.", Client_1, '2')
                    grab_input(Client_2)
            case False:
                    send(board_str(), False, '12')
                    send("Waiting on other player.", Client_2, '2')
                    grab_input(Client_1)

                    send(board_str(), False, '12')
                    send("Waiting on other player.", Client_1, '2')
                    grab_input(Client_2)





def game_main():
    
    
    if "Client_1_First" not in globals():
        global Client_1_First
        Client_1_First = bool(randrange(0, 2))
    
    wait(1.5)

    game()

    
    




def main():
    global restart
    while True:

        restart = False

        if 'Server' not in globals():
            global Server
            Server = create_socket(2)


        # getting ready for players
        global Client_1, Client_2
        Client_1, addr1 = Server.accept()
        print(f"Connected to first client {addr1}")
        send("Waiting for Second Player", Client_1, "2")
        if restart == False:
            Client_2, addr2 = Server.accept()
            print(f"Connected to second client {addr2}")
            send("Welcome to Tik Tak Toe!", False, '12')
        if restart == False:
            game_main()

    


        







if __name__ == '__main__':
    print("Start of server program")
    main()