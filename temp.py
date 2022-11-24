import sys
from pynput import keyboard

keys = keyboard.Controller()

num_str = ""

def read_num(key):
    global num_str
    if key == keyboard.Key.enter:
        print("enter pressed,quit:",num_str)
        return False
    if key == keyboard.Key.backspace:
        num_str = num_str[:len(num_str)-1]
    elif key.char in '1234567890':
        num_str += key.char
        print(num_str)
    

def test_input():
    with keyboard.Listener(on_press=read_num) as lis:
        print("input start")
        lis.join()
        
    print(num_str)

def exit():
    sys.exit()

with keyboard.GlobalHotKeys({"<ctrl>+<alt>+I":test_input,"<ctrl>+C":exit}) as h:
    h.join()