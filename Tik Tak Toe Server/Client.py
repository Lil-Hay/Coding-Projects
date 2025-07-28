import socket
import struct
from os import system
# function to grab user input, checks to make sure user input is an int
def grab_user_input(type=int): 

    if type == int:
        while True:
            try: 
                user_input = int(input())
            except:
                print('Please enter a number, EX.("8")')
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
        Comm.connect((socket.gethostbyname(socket.gethostname()), 9090))

    except: # if connection can't be made
       reconnect_attempts += 1
       reconnect()

    else: # if connection is made tell user of it and start main loop for program
        #Comm.settimeout(2.0) # set timeout to check for dissconnects/second messages
        print("Connection Succeseful")
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



# receive fuction
def receive():
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

        if Server_message.find('TYPE=STR') != -1:
            Server_message = Server_message.replace('TYPE=STR', '')
            status = str

        if Server_message.find('SECOND_MESSAGE') != -1:
            Server_message = Server_message.replace('SECOND_MESSAGE', '')
            print(Server_message)
            already_print = True
            status = receive()

        if already_print != True:
            print(Server_message)

        return status


                
                

        # Add future elif statements for other edge cases that sever sends

def new_receive():
    status = False
    # Display server's message
    try: # try catch to handle lost connection
        Server_message = Comm.recv(1024).decode("utf-8")

    except:
        print("Looks like connection failed on receive")
        return True # return true to end main loop
    
    else:
        Server_message.find("")


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
    
    reconnect() # check if user wishes to reconnect



if __name__ == '__main__':
    connect()
