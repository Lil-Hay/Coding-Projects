# the goal of this program is to create an interactive terminal game using the input class
# first we declare a variable called username that will ask for their username which we will call them by for the rest of this program

username = input("Please enter your username: ")

# welcome the player and present them with their first task in this game a choice...
print("Welcome " + username + "!" + "\n" +
      "Your goal for this game is to get the highest score by making the best decisions.")
first_decicion = input(
    "You're presented with two paths, one leads towards a forest (1) the other a peaceful looking town (2) what do you do? ")

# set the score based off their first decicion and declare a variable named "score" that will be used through the rest of this
if first_decicion == "2":
    score = 10
else:
    score = 0

# second decicion and now we start either adding to the score or leaving it
second_decicion = input(
    "you can eat a apple (1) or a slice of pizza (2) what do you do? ")

if second_decicion == "1":
    score = score + 10

# end the game and tell them their score

# first we're going to make "score" a string so it will print to the terminal
score = str(score)

# now we print to the terminal
print(username + " your score is " + score + "!" + "\nThanks for playing!")

# soltion to game closing before you can read your final score
exitgame = input("press enter to exit: ")
