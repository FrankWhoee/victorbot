import pyperclip
import time
from pyautogui import press,hotkey

shakespeare = open("poems/shake2.txt", "r")
shakespeare = shakespeare.read().split("\n")

for i in shakespeare:
    time.sleep(len(i) * 0.125)
    pyperclip.copy(i)
    hotkey("ctrl","v")
    press("enter")