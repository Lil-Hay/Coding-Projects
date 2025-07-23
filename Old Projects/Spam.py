from pynput import mouse
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time
import pygetwindow as gw

# setup variables for keypresses, main loop, and user spam messages
keyboard = KeyboardController()
mouse = MouseController()

run_application = True

user_message = input("Please enter what you would like spammed: ")

# grab interval to use and prevent app from messing up
user_error = True
while user_error == True:

    try:
        user_interval = int(
            input("Please enter how long between sending messages(Please make it more than 2 so it doesn't go crazy!): "))

        if user_interval <= 2:
            print("Please enter more than 2 to prevent it going haywire")
        else:
            user_error = False

    except:
        print("Please enter a number")


# make sure discord is open
discord_open = False
while discord_open == False:
    try:
        discord = gw.getWindowsWithTitle('Discord')[0]
        discord_open = True
    except:
        print("Please open discord, Trying again in 10 seconds.")
        time.sleep(10)

# grab message box postion
print("Please ensure you have Discord is fullscreened, I'm going to grab the message box postion\nPlease hover your mouse over the message box, you'll have 5 seconds to do this")
input("Press enter when ready: ")
time.sleep(5)
message_box = mouse.position
input("Spam will start as soon as you press enter, Please make sure you have the right chat opened: ")

# main loop
while run_application == True:

    # make sure discord is open
    discord_open = False
    while discord_open == False:
        try:
            discord = gw.getWindowsWithTitle('Discord')[0]
            discord_open = True
        except:
            print("Please open discord, Trying again in 10 seconds.")
            time.sleep(10)

    # open discord and fullscreen
    discord.restore()
    discord.maximize()
    discord.activate()

    # click into window to type
    mouse.position = (message_box)
    mouse.click(Button.left, 1)

    # type stuff in discord
    keyboard.type(user_message)
    keyboard.press(Key.enter)

    # wait specified amount of seconds and tell how long has elapsed
    print("Sending message again in %s seconds", user_interval)
    time_pass = 0
    while time_pass < user_interval:
        time.sleep(1)
        time_pass = time_pass + 1
        print(time_pass)
