# this is an 8ball program
def main():

    # Mini Games Stuff
    from time import sleep as pause
    import random
    import Main_Menu
    from os import system

    # we need the random function to get random 8 ball answers

    # we need the time function to keep the application from closing instantly

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

        # ignore uppercase so we can answer the same question in both cases
        user_answer = user_answer.lower()

        # if they don't enter anything say "invalid answer" and don't give them an answer
        if user_answer == "":
            print("invalid answer")
            pause(0.5)

        # Easter Egg
        elif user_answer == "am i gay?":
            print(
                "Very funny that you ask me that, well the truth is you are Gay, Ok now get over it!")
            pause(0.5)

        # Easter Egg
        elif user_answer == "am i fat?":
            print("Mad Fat Dawg!")
            pause(0.5)

        # valid question so we give them a random 8ball answer
        else:
            print(random.choice(_8ball_says))
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