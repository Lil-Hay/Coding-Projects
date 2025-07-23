from time import sleep
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button, Controller, Listener
from pynput.keyboard import Controller as keyboard_controller
import webbrowser
import os
import pygetwindow as gw

keyboard = keyboard_controller()
mouse = Controller()

os.startfile('notepad.exe')


sleep(0.1)

notepad = gw.getWindowsWithTitle('Untitled')[0]

notepad.restore()
notepad.maximize()
notepad.activate()

x = 0
while x < 50:
    x =+ 1
    keyboard.type('Stupid, Why would you run this?!')

sleep(2)
webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 2, True)

sleep(4)

mouse.position = (739, 572)
mouse.click(Button.left, 1)

sleep(5)

#os.system("shutdown /s /t 1")
