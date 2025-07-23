# this is an 8ball program

# possible answers for the 8ball
_8ball_says = [
        "Heck Nah!",
        "Heck Yeah!",
        "Most Likely.",
        "Depends What You Think.",
        "I Don't Know, Are You?",
        "Why Are You Asking Me!",
        "Probably.",
        "Unfortunately.",
        "Definitly.",
        "Indeed."
    ]

def response(user_answer=str):
    from random import choice as random
    user_answer = user_answer.lower()
    match user_answer:
        case "":
            return "invalid answer"
        case user_answer if 'am i gay' in user_answer: 
            return "Very funny that you ask me that, well the truth is you are Gay, Ok now get over it!"
        case user_answer if 'am i fat' in user_answer:
            return 'Mad Fat Dawg!'
        case _:
            return random(_8ball_says)
            
   

def main():

    # Mini Games Stuff
    from time import sleep as pause
    import Main_Menu
    from os import system

    # we need the random function to get random 8 ball answers

    # we need the time function to keep the application from closing instantly

    # introduce the player to the program
    print("Shake the 8ball and I will answer you!")
    pause(0.5)

    # we'll use this variable to keep the main loop going until it changes to false
    user_play = True

    # we'll use a while loop to allow them to go forever
    while user_play == True:

        # let them ask a question
        user_answer = input("What do you ask?\n")
        pause(0.5)

        print(response(user_answer)) # use repsonse function to print a response
        pause(0.5)

        # this is where they can break the loop by saying "n" and end the application we'll also use a nested loop to prevent an invalid answer

        # declare booleon to use for nested loop
        invalid_answer = True

        # nested loop so if they answer invalidly to leaving the application it'll keep asking them for a valid answer
        while invalid_answer == True:

            try:
                user_answer = int(
                    input('Do you want to Play Again (1), Return to Main Menu (2), or Exit (3)?\n'))
                pause(0.5)

                if user_answer == 1:
                    invalid_answer = False
                    print("Playing Again")
                    pause(0.5)
                    system("cls")

                elif user_answer == 2:
                    invalid_answer = False
                    user_play = False
                    print("Returning to Main Menu")
                    pause(0.5)
                    system("cls")
                    Main_Menu.main()

                elif user_answer == 3:
                    invalid_answer = False
                    user_play = False
                    print("Exiting Program\nThanks For Playing!")
                    pause(1)

                else:
                    print('Invalid Answer, Please enter a number between "1" and "3"')
                    pause(0.5)

            except:
                print('Invalid Answer, Please enter a number between "1" and "3"')
                pause(0.5)

        # end of check play again loop





def main_server(send, receive):

    send("Shake the 8ball and I will answer you!"
        "\nWhat will you ask?")
    
    while True:
        
        user_input = receive(str)
        send(response(user_input) + 
             '\nDo you want to Play Again (1), Return to Main Menu (2), or Exit (3)?')

        while True:
            user_input = receive()
            match user_input:
                case 1: # play again
                    send('What will you ask?')
                    break
                case 2: # return to main menu loop
                    return
                case 3: # exit
                    return False 
                case _: # invalid answer
                    send('Invalid Answer, Please enter a number between "1" and "3"')


if __name__ == '__main__':
    main()