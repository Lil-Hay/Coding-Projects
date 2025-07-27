from Tik_Tak_Toe import main as Tik_Tak_Toe
from _8Ball import _8ball
from Rock_Paper_Scissors import Rock_Paper_Scissors
from Hangman import hangman
from Number_Guess import Number_Guess

def main():
    def cls():
        system('cls')

    from time import sleep as pause
    from os import system

    while True:
        try:
            user_select = int(input(
                'Available Mini-Games: '
                '\n8Ball (1)'
                '\nNumber Guessing Game (2)'
                '\nRock, Paper, Scissors (3)'
                '\nHangman (4)'
                '\nTik Tak Toe (5)'
                '\nPlease enter the number that corraspondes with the game you want to play or use "6" to exit: \n'))
            pause(0.5)
        except:
            print("Please enter a valid answer")
            pause(0.5)

        match user_select:
            case 1:
                cls()
                _8ball.main()
                return
            case 2:
                cls()
                Number_Guess.main()
                return
            case 3:
                cls()
                Rock_Paper_Scissors.main()
                return
            case 4:
                cls()
                hangman.main()
                return
            case 5:
                cls()
                Tik_Tak_Toe.main()
                return
            case 6:
                print("Thanks for Playing!")
                pause(1)
                return
            case _ :
                print("There was an Error!")
                pause(2)

if __name__ == "__main__":
    main()
