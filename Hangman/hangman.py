import random
from os import system
from time import sleep


# Clear screen also has argument for waiting to clear screen
def cls(pause_time=0):

    sleep(pause_time)
    system('cls')


# Choose random word from words file
def choose_word():

    with open('words.txt', 'r') as file:
        word = file.readlines()
        word = random.choice(word).strip()

    return word


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


# main for game logic
def game():

    magic_word = choose_word()
    user_progress = coded_word(magic_word)
    print(user_progress)
    User_guesses = 0

    # main loop for each guess
    while User_guesses < 10:

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
                print(f"Current progress: {user_progress}" + f" You have {10 - User_guesses} guesses left.")

        # if user wants to guess whole word
        elif user_choice == '2':

            if guess_word(magic_word, user_progress) == True:
                cls()
                print(f"Congratulations! You've guessed the word correctly! The word was: {magic_word}")
                break

            else:
                User_guesses += 1
                cls()
                print(f"Incorrect guess. You have {10 - User_guesses} guesses left." + f"\ncurrent progress: {user_progress}")

        # if user doesn't make valid choice
        else:
            print("Invalid choice. Please choose 1 for letter or 2 for word.")
            cls(1.5)

    # if user doesn't guess in time
    if User_guesses == 10:
        print(f'You failed to guess the word in time. The word was "{magic_word}"')


# main for program
def main():

    print("Welcome to Hangman!")
    print("Try to guess the word letter by letter or by guessing the whole word!")
    
    # main game logic
    game()

    # play again loop
    while True:
        user_input = input("Would you like to play again Y/N?: ")
        if user_input.lower() == 'y':
            game()
        elif user_input.lower() == 'n':
            break
        else:
            print("Please enter a valid answer (Y/N)")





if __name__ == "__main__":
    main()