# decide winner function
def Decide_Winner(Ai, Player):
    if Ai == Player:
        winner = "None"
    elif Ai == "Rock" and Player == "Paper":
        winner = "player"
    elif Ai == "Rock" and Player == "Scissors":
        winner = "ai"
    elif Ai == "Paper" and Player == "Scissors":
        winner = "player"
    elif Ai == "Paper" and Player == "Rock":
        winner = "ai"
    elif Ai == "Scissors" and Player == "Rock":
        winner = "player"
    elif Ai == "Scissors" and Player == "Paper":
        winner = "ai"
    return winner


# main version of game
def main():

    import random
    from time import sleep as pause
    import Main_Menu
    from os import system

    # introduce player to game
    print("Welcome to Rock, Paper, Scissors!")
    pause(0.5)

    options = ['Rock', "Paper", "Scissors"]

    Wins = 0
    Losses = 0
    Ties = 0 


    # main game loop (this will allow for multiple games)

    user_play = True
    while user_play == True:

        # generate Ai choice
        Ai_choice = random.choice(options)

        # loop to check for valid player answer and gather their answer
        user_input_error = True

        # little variabel so it doesn't give an error message after first invalid answer
        user_error_count = 0

        # putting this here so it doesn't get spammed in the loop
        print('Please enter Rock (1), Paper (2), Or Scissors (3)')
        pause(0.5)

        while user_input_error == True:

            try:
                User_choice = int(input())

                # if user gives vaild answer
                if User_choice == 1:
                    User_choice = "Rock"
                    user_input_error = False
                elif User_choice == 2:
                    User_choice = "Paper"
                    user_input_error = False
                elif User_choice == 3:
                    User_choice = "Scissors"
                    user_input_error = False

                # if user gives invalid answer
                else:
                    if user_error_count == 0:
                        user_error_count = user_error_count + 1
                        print('Invalid Answer, Please enter a Number between "1" and "3"')
                        pause(0.5)
                    else:
                        continue

            except:
                if user_error_count == 0:
                    user_error_count = user_error_count + 1
                    print('Invalid Answer, Please enter a Number between "1" and "3"')
                    pause(0.5)
                else:
                    continue

        # end of valid choice loop

        # use decide winner function to compare Ai and Player's choices and store it as a variable
        winner = Decide_Winner(User_choice, Ai_choice)

        # if neither wins
        if winner == "None":
            Ties = Ties + 1
            print("You Tied!\nThe Ai chose", Ai_choice, "\nYou chose", User_choice,
                "\nYou have", Wins, "Wins,", Losses, "Losses, and", Ties, "Ties!")
            pause(0.5)

        # if Ai wins
        elif winner == "ai":
            Losses = Losses + 1
            print("You Lost!\nThe Ai chose", Ai_choice, "\nYou chose", User_choice,
                "\nYou have", Wins, "Wins,", Losses, "Losses, and", Ties, "Ties!")
            pause(0.5)

        # if player wins
        elif winner == "player":
            Wins = Wins + 1
            print("You Won!\nThe Ai chose", Ai_choice, "\nYou chose", User_choice,
                "\nYou have", Wins, "Wins,", Losses, "Losses, and", Ties, "Ties!")
            pause(0.5)
        
        # Error in program deciding winner
        else:
            print("Error In Deciding Winner, Please Contact The Creator of This Program")

        # ask player if they want to continue playing
        user_input_error = True
        while user_input_error == True:
            try:
                User_choice = int(
                    input("Do you want to Play Again (1), Return to Main Menu (2), Or Exit (3)?\n"))
                pause(0.5)

                if User_choice == 1:
                    user_input_error = False
                    print("Continuing Game")
                    pause(0.5)
                    system("cls")

                elif User_choice == 2:
                    user_input_error = False
                    user_play = False
                    print("Returning to Main Menu")
                    pause(0.5)
                    system("cls")
                    Main_Menu.main()

                elif User_choice == 3:
                    user_input_error = False
                    user_play = False
                    print("Exiting Program\nThanks For Playing!")
                    pause(1)

                else:
                    print('Invalid Answer, Please enter a Number between "1" and "3"!')
                    pause(0.5)

            except:
                print('Invalid Answer, Please enter a Number between "1" and "3"!')
                pause(0.5)

        # end of asking player if they want to continue
    # end of main game loop





def main_server(send, receive):
    from random import choice as random
    send("Welcome to Rock, Paper, Scissors!"
         '\nPlease enter Rock (1), Paper (2), Or Scissors (3)')
    
    options = ['Rock', "Paper", "Scissors"]

    # variables for keeping score of there wins and losses
    Wins = 0
    Losses = 0
    Ties = 0



    user_choice = str

    # main game loop
    while True:
       
        ai_choice = random(options)

        # grab user choice
        while True:
            user_input = receive()
            
            match user_input:
                case 1:
                    user_choice = 'Rock'
                    break
                case 2:
                    user_choice = 'Paper'
                    break
                case 3:
                    user_choice = 'Scissors'
                    break
                case _:
                    send("Please enter a valid answer between 1 and 3")

        # decide winner
        winner = Decide_Winner(ai_choice, user_choice)

        match winner:

            case 'ai':
                Losses += 1
                send(f'You Lost!\nThe Ai chose: {ai_choice}\nYou chose: {user_choice}'
                     f'\nYou have {Wins} Wins, {Losses} Losses, and {Ties} Ties'
                     '\nDo you want to Play Again (1), Return to Main Menu (2), Or Exit (3)?')
                
            case 'player':
                Wins += 1
                send(f'You Won!\nThe Ai chose: {ai_choice}\nYou chose: {user_choice}'
                     f'\nYou have {Wins} Wins, {Losses} Losses, and {Ties} Ties'
                     '\nDo you want to Play Again (1), Return to Main Menu (2), Or Exit (3)?')
                
            case 'None':
                Ties += 1
                send(f'You tied!\nThe Ai chose: {ai_choice}\nYou chose: {user_choice}'
                     f'\nYou have {Wins} Wins, {Losses} Losses, and {Ties} Ties'
                     '\nDo you want to Play Again (1), Return to Main Menu (2), Or Exit (3)?')
                
            case _:
                send('Something went wrong, contact creator of this program'
                     '\nDo you want to Play Again (1), Return to Main Menu (2), Or Exit (3)?')
        

        # play again loop
        while True:
            user_input = receive()
            
            match user_input:
                case 1:
                    send('Please enter Rock (1), Paper (2), Or Scissors (3)')
                    break
                case 2:
                    return
                case 3:
                    return False
                case _:
                    send('Please enter a number between "1" and "3"')
        


if __name__ == '__main__':
    main()