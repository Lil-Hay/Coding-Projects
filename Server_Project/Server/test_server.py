import socket
import struct
from _8ball import main_server as _8ball
from Number_Guess import main_server as Number_Guess
from Rock_Paper_Scissors import main_server as Rock_Paper_Scissors

def create_socket():
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket object
    try:            
        # bind ip (first arg) and port (second arg) to socket.
        # IP should be '0.0.0.0' for production.
        # Local host is socket.gethostbyname(socket.gethostname())
        Socket.bind((socket.gethostbyname(socket.gethostname()), 9090))
    except:
        print("handled bind exception") 
    else:
        Socket.listen(1) # allows for one connection at time and listens for connections
        return Socket 

# function to send a message to client
def send(message):

    inside_message = message.encode('utf-8') # need to enocode the data

    try: # try catch so server doesn't crash with unhandled exception
        Comm.sendall(inside_message)

    except:
        print("Connection Lost on send")
        main('lost')

# receive function 
def receive(type=int):
    if type == int:
        try: #try catch to prevent server from crashing due to unhandled exception
            encoded_transmission = Comm.recv(4) #receive data from client
            decoded_transmission = struct.unpack('!i', encoded_transmission)[0] #decode int from client
            return int(decoded_transmission) #return back int to use with other fuctions
    
        except: #handle exception
            print("Connection Lost on receive")
            main('lost') #return something so fuctions know connection is lost
            
    if type == str:
        try:
            return Comm.recv(1024).decode('utf-8')
        except:
            print("Connection Lost on receive")
            main('lost')

    

# ask for password function
def ask_for_password():

    send("Please enter the password") # tell user to enter password
    
    user_tries = 1 #keeps track of attempts

    while True: 
        
        user_input = receive() #use receive fuction to assign user's input to variable
        
        if user_input == 5050: # check for correct password
            print("recognized correct password") 
            send("Correct password, entering main menu") # tells user they have the correct password
            return True # return True if user gets password
        
        elif user_tries == 5: # if user fails too many times
            send("Too many failed attempts, ending connection") #this will tell client to close down
            print("User has failed too many times, terminating connection") #print to log that user failed password checks
            return False # returns False for this fuction to tell main loop that they failed
        
        elif user_input == "connection lost": # what to do if connection lost
            return False # also returns False so it can close connection
        
        else: # Just tells us how many times they failed and tells user they failed
            print(f"User failed password check, total tries:{user_tries}")
            send("Wrong password please try again")
            user_tries = user_tries + 1

def main_menu():
    while True:
        send('Welcome to Mini Games!'
        '\nAvailable Mini-Games\n8Ball (1)'
        '\nNumber Guessing Game (2)'
        '\nRock, Paper, Scissors (3)'
        '\nPlease enter the number that corraspondes with the game you want to play or use "4" to exit connection.')
        message = receive()

        match message:

            case 1: # 8 Ball game

                if _8ball(send, receive) == False: # if 8 ball program returns false we exit
                    send ('close client')
                    return
                
            case 2: # Number Guessing game

                if Number_Guess(send, receive) == False:
                    send('close client')
                    return
                
            case 3: # Rock, Paper, Scissors game (not implamented yet)
                
                if Rock_Paper_Scissors(send, receive) == False:
                    send('close client')
                    return
            
            case 4: # close client
                send("close client")
                return
            
            case _: # invalid answer
                send("Please enter a valid answer")
                message = receive()
                





# main server loop that keeps running 
def main(connection=None):
    if connection == 'lost':
        print('looking for new connections')
    while True:

        if 'Server' not in globals(): # create Server object that can be assigned a connection
            global Server
            Server = create_socket()
            print("looking for connections")
        

        global Comm
        Comm, addr = Server.accept() # accepts a connection and print address while assighing "Comm" as  the connection
        print(f"connected to: {addr}")

        Unlocked = ask_for_password() # runs fuction to check for password and assigns a true or false value

        if Unlocked == False: # user failed password check closes out connection
            Server.close
            print("looking for new connection")

        if Unlocked == True: # user passed password check
            print("user passed")
            main_menu()
            print("done with Main Menu\nlooking for new connections")
        
if __name__ == '__main__':
    print('start of server program')
    main()        