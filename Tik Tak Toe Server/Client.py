import socket
import struct
from os import system
from time import sleep
# function to grab user input, checks to make sure user input is an int
def grab_user_input(type=int): 

    if type == int:
        while True:
            try:
                user_input = int(input())
            except:
                system('cls')
                print("Please enter a number not text")
                sleep(1.5)
                system("cls")
                for I in message_history:
                    print(I)
            else:
                return user_input
    if type == str:
        user_input = input()
        return user_input



# connect function
def connect(): 

    if 'reconnect_attempts' not in globals():
            global reconnect_attempts
            reconnect_attempts = 0

    global Comm # make globel so other fuctions can use object "Comm" to execute send and receive
    Comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # use create socket function to make a new socket

    #connect to server
    try: # try catch in case connection can't be made
        # first arg is ip second is port
        # ip of server 192.168.1.149
        # Local host is socket.gethostbyname(socket.gethostname())
        Comm.connect("192.168.1.149", 9090))

    except: # if connection can't be made
       reconnect_attempts += 1
       reconnect()

    else: # if connection is made tell user of it and start main loop for program
        #Comm.settimeout(2.0) # set timeout to check for dissconnects/second messages
        system('cls')
        print("Connection Succeseful... Waiting for a response from server.")
        reconnect_attempts = 0
        Main()



# used to send stuff to server
def send(message):

    if message == int:
        user_input = grab_user_input(int)
        input_encoded = struct.pack('!i', user_input) # pack up int for transmission to server


        try: # try catch to handle if connection is lost
            Comm.sendall(input_encoded)

        except:
            print("Looks like connection failed on send")
            return True # return true to end main loop
        
    if message == str:
        user_input = grab_user_input(str)

        try:
            user_input = user_input.encode('utf-8')
            Comm.sendall(user_input)

        except:
            print("Looks like connection failed on send")
            return True # return true to end main loop

def delete_msg_history(all=False):

    if all == True:
        for I in message_history:
            message_history.pop()
    else:
        for I in message_history:
            try:
                message_history.remove('Waiting for Second Player')
            except:
                pass
            try:
                message_history.remove('Welcome to Tik Tak Toe!')
            except:
                pass
        

# receive fuction
def receive():
    if 'message_history' not in globals():
        global message_history
        message_history = []
    if message_history != None:
        delete_msg_history()
        
    status = False
    # Display server's message
    try: # try catch to handle lost connection
        Server_message = Comm.recv(1024).decode("utf-8")

    except:
        print("Looks like connection failed on receive")
        return True # return true to end main loop
    
    else: 

        if Server_message.find('CLEAR_SCREEN') != -1:
            system('cls')
            Server_message = Server_message.replace('CLEAR_SCREEN', '')

        if Server_message.find('DISCONNECT') != -1:
            Server_message = Server_message.replace('DISCONNECT', '')
            print(Server_message)
            print("Server wishes to Disconnect")
            return True
        
        if Server_message.find('TYPE=STR') != -1:
            Server_message = Server_message.replace('TYPE=STR', '')
            status = str

        if Server_message.find('SECOND_MESSAGE') != -1:
            Server_message = Server_message.replace('SECOND_MESSAGE', '')
            message_history.append(Server_message)
            print(Server_message)
            already_print = True
            status = receive()

        

        try:
            if already_print != True:
                message_history.append(Server_message)
                print(Server_message)
        except:
            print(Server_message)
            message_history.append(Server_message)

        return status


                
                

        # Add future elif statements for other edge cases that sever sends


# reconnect function
def reconnect():

    break_loop = False # declared boolean to break out of loops in loops

    if reconnect_attempts == 5:
        break_loop = True
        print("Looks like the connection was unsuccessful\nToo many attempts to connect... exiting program")
        return
    
    print("looks like there is no connection.\nEnter 1 to start new connection or enter 2 to end program:")

    while break_loop == False:

        user_input = grab_user_input()

        if user_input == 1: # reconnect
            Comm.close() # close out current Commet
            break_loop = True # set this to true to break this loop for exiting out
            connect() # create new connection
        elif user_input == 2: # Exit
            break_loop = True # set this to true to break this loop
        else: # user doesn't enter valid answer
            print("Please enter a valid input")


# Main Loop
def Main():
    
    while True: # infinite loop
        type = int
        server_response = receive()
        if server_response == True: # receive will return True if something goes wrong
            break
        if server_response == str:
            type = str
        if send(type) == True: # Send will return True if something goes wrong
            break
        delete_msg_history(True)
    
    reconnect() # check if user wishes to reconnect



if __name__ == '__main__':
    connect()
