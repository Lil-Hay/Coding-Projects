import random
import os
from time import sleep
import Main_Menu


# Clear screen also has argument for waiting to clear screen
def cls(pause_time=0):

    sleep(pause_time)
    os.system('cls')


# Choose random word from words file
def choose_word():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        words_path = os.path.join(script_dir, 'words.txt')
        with open(words_path, 'r') as file:
            word = file.readlines()
            word = random.choice(word).strip()
            return word
    except FileNotFoundError:
        print("Error: 'words.txt' file not found. Please ensure the file exists in the same directory as this script.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    


# Function for user to guess whole word
def guess_word(magic_word=str, user_progress=str):

    cls()
    print(user_progress)
    magic_word_lower = magic_word.lower()
    guess = input("Guess the word: ").lower()

    if guess == magic_word_lower:
        return True
    else:
        return False


# Function to replace underscores in "user_progress" with correctly guessed letters
def replace_letter(magic_word=str, user_progress=str, user_guess=str):

    used_index = 0
    magic_word_lower = magic_word.lower()
    magic_word_list = list(magic_word)
    new_user_progress = user_progress
    interation = 0

    while True:
        positon = magic_word_lower.find(user_guess, used_index)

        if positon == -1:
            return new_user_progress
        
        new_user_progress_list = list(new_user_progress)

        if positon == 0:
            new_user_progress_list[positon] = magic_word_list[positon]
            used_index = positon + 1
            new_user_progress = ''.join(new_user_progress_list)

        else:
            new_user_progress_list[positon * 2] = magic_word_list[positon]
            used_index = positon + 1
            new_user_progress = ''.join(new_user_progress_list)
            interation += 2
            

# Function for user to guess each letter
def guess_letter(magic_word=str, user_progress=str):
    
    cls()
    print(user_progress)
    user_guess = input("Guess a letter: ")
    user_guess_lower = user_guess.lower()
    new_user_progress = replace_letter(magic_word, user_progress, user_guess_lower)

    if new_user_progress == user_progress:
        print(f'The letter "{user_guess}" was not found in the word')
    else:
        print(f'The letter "{user_guess}" was found in the word')
    
    return new_user_progress


# function to turn the word into a coded word that user can guess off of
def coded_word(magic_word):

    length_of_word = len(magic_word)
    coded_word = ''
    x = 0

    for letter in magic_word:

        if x == (length_of_word) - 1:
            coded_word += '_'
            return coded_word
        
        if letter == ' ':
            coded_word += '  '
        else:
            coded_word = coded_word + '_ '
        
        x += 1


# check if user has guessed enough letter to complete word
def user_progress_equals_word(magic_word=str, user_progress=str):

    user_progress_list = list(user_progress)
    position = 0
    for letter in magic_word:
        if letter == user_progress_list[position]:
            position += 2
        else:
            return False
    return True
def choose_diffuclty():
    while True:
        user_input = input("Choose difficulty level (1 for easy, 2 for medium, 3 for hard): ")
        if user_input == '1':
            return 16  # Easy
        elif user_input == '2':
            return 12   # Medium
        elif user_input == '3':
            return 8   # Hard
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

# main for game logic
def game():

    magic_word = choose_word()
    if magic_word is None:
        print("Game cannot start without a valid word. Exiting.")
        sleep(2)
        return True
    user_progress = coded_word(magic_word)
    diffuclty = choose_diffuclty()
    print(user_progress)
    User_guesses = 0



    # main loop for each guess
    while User_guesses < diffuclty:

        user_choice = input("Would you like to guess a letter or the whole word? (1 for letter, 2 for word): ")

        # if user wants to guess letter
        if user_choice == '1':

            user_progress = guess_letter(magic_word, user_progress)

            if user_progress_equals_word(magic_word, user_progress) == True:
                cls(1.5)
                print(f"Congratulations! You've guessed the word correctly! The word was: {magic_word}")
                break

            else:
                User_guesses += 1
                cls(1.5)
                print(f"Current progress: {user_progress}" + f" You have {diffuclty - User_guesses} guesses left.")

        # if user wants to guess whole word
        elif user_choice == '2':

            if guess_word(magic_word, user_progress) == True:
                cls()
                print(f"Congratulations! You've guessed the word correctly! The word was: {magic_word}")
                break

            else:
                User_guesses += 1
                cls()
                print(f"Incorrect guess. You have {diffuclty - User_guesses} guesses left." + f"\ncurrent progress: {user_progress}")

        # if user doesn't make valid choice
        else:
            print("Invalid choice. Please choose 1 for letter or 2 for word.")
            cls(1.5)

    # if user doesn't guess in time
    if User_guesses == diffuclty:
        print(f'You failed to guess the word in time. The word was "{magic_word}"')


# main for program
def main():

    print("Welcome to Hangman!")
    print("Try to guess the word letter by letter or by guessing the whole word!")
    
    # main game logic
    if game() == True:
        return

    # play again loop
    while True:
        try:
            user_input = int(input("Would you like to play again (1), Return to Main Menu (2), or Exit (3): "))
            if user_input == 1:
                game()
            elif user_input == 2:
                cls()
                Main_Menu.main()
                break
            elif user_input == 3:
                return
            else:
                print("Please enter a valid answer")
        except:
            print("Please enter a valid answer")





if __name__ == "__main__":
    main()