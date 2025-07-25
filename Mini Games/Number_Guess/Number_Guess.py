def main():

    import Main_Menu
    import random
    from time import sleep as pause
    from os import system

    random_number = random.randint(0, 100)
    score = 50
    user_play = True
    user_input = str

    # rules explained at beginning
    print("Please enter a number between 0 and 100, your score starts at 50 but for every guess wrong 1 is subtracted!")
    pause(0.5)

    # main loop for program to allow for multiple games
    while user_play == True:

        # check for right answer loop
        user_guess_right = False

        while user_guess_right == False:

            # ask for answer and catch an invalid type
            user_give_string = True
            while user_give_string == True:
                try:
                    user_input = int(input())
                    user_give_string = False
                except:
                    print(
                        "Invalid answer. Make sure to keep it between 0 and 100 and use numbers")
                    pause(0.5)
                    score = score - 1
            # end of asking for answer and catch error loop

            # tell them if it's higher, lower, or correct
            if user_input == random_number:

                # if they get it right

                # easter egg
                if user_input & random_number == 69:
                    print("Congrats you got it right it was",
                        random_number, "Nice!", "Your score is", score)
                    pause(0.5)
                    user_guess_right = True

                # what will normally happen
                else:
                    print("Congrats you got it right it was",
                        random_number, "Your score is", score,)
                    pause(0.5)
                    user_guess_right = True

            # if they get it wrong

            elif user_input > random_number:
                print("Wrong the number is less than", user_input)
                score = score - 1
                pause(0.5)

            elif user_input < random_number:
                print("Wrong the number is more than", user_input)
                score = score - 1
                pause(0.5)

        # asking user if they want to continue playing
        user_continue_invalid = True
        while user_continue_invalid == True:
            try:
                user_play_answer = int(
                    input('Do you want to Play Again (1), Return to Main Menu (2), or Exit (3)?\n'))
                pause(0.5)

                if user_play_answer == 3:
                    user_play = False
                    user_continue_invalid = False
                    print("Exiting Program\nThanks For Playing!")
                    pause(1)
                elif user_play_answer == 2:
                    print("Returning to Main Menu")
                    user_continue_invalid = False
                    user_play = False
                    pause(0.5)
                    system("cls")
                    Main_Menu.main()
                elif user_play_answer == 1:
                    score = 50
                    random_number = random.randint(0, 100)
                    system("cls")
                    print("Please enter a number")
                    pause(0.5)
                    user_continue_invalid = False
                else:
                    print('Please enter a number between "1" and "3"')
                    pause(0.5)
            except:
                print('Invalid Answer, Please enter a number between "1" and "3"')
                pause(0.5)
        # end of play again loop
    # end of main loop