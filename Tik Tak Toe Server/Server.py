import struct
import socket
from time import sleep as wait
from random import randrange





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
    else:        
        try: # try catch so server doesn't crash with unhandled exception
            Client.send(message.encode('utf-8'))
        except:
            print("Connection Lost on send")
            main()
            return


def receive(client, type=int):
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
            
    if type == str:
        try:
            return client.recv(1024).decode('utf-8')
        except:
            print("Connection Lost on receive")
            main()
            return

def game():
    send('This is a test to see if connection still works here', False, '12')








def game_main():
    if 'Stats' not in globals():
        global Stats
        Stats = [0, 0, 0] #[0] = Wins, [1] = losses, [2] = ties
    
    if "Client_1_First" not in globals():
        global Client_1_First
        Client_1_First = bool(randrange(0, 2))
    
    wait(1.5)

    game()

    
    




def main():
    
    while True:
        if 'Server' not in globals():
            global Server
            Server = create_socket(2)


        # getting ready for players
        global Client_1, Client_2
        Client_1, addr1 = Server.accept()
        print(f"Connected to first client {addr1}")
        send("Waiting for Second Player", Client_1, "2")
        Client_2, addr2 = Server.accept()
        print(f"Connected to second client {addr2}")
        send("Welcome to Tik Tak Toe!", False, '12')

        game_main()

    


        







if __name__ == '__main__':
    print("Start of server program")
    main()