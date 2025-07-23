def main():

    from time import sleep as pause
    import _8ball, Number_Guess, Rock_Paper_Scissors
    from os import system
    
    accepted_answer = False
    while accepted_answer == False:
        try:
            user_select = int(input(
                'Available Mini-Games\n8Ball (1)\nNumber Guessing Game (2)\nRock, Paper, Scissors (3)\nPlease enter the number that corraspondes with the game you want to play or use "4" to exit.\n'))
            pause(0.5)

            if user_select == 1 or user_select == 2 or user_select == 3 or user_select == 4:
                accepted_answer = True
            else:
                print("Please enter a valid answer")
                pause(0.5)

        except:
            print("Please enter a valid answer")
            pause(0.5)

    if user_select == 1:
        system("cls")
        _8ball.main()

    elif user_select == 2:
        system("cls")
        Number_Guess.main()

    elif user_select == 3:
        system("cls")
        Rock_Paper_Scissors.main()

    elif user_select == 4:
        print("Thanks for Playing!")
        pause(1)
        
    else:
        print("There was an Error!")
        pause(2)
