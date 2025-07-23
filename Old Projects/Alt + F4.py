from time import sleep
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pygetwindow as gw

count = 0
keyboard = Controller()

terminal = gw.getWindowsWithTitle('Python')[0]
terminal.minimize()
sleep(1)

while count == 0:

	keyboard.press(Key.alt)
	keyboard.press(Key.f4)
