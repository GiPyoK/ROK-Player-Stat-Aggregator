import pyautogui as pg
import os
import pyperclip


if not os.path.exists("player images"):
    os.makedirs("player images")

os.chdir("player images")

names_dict = {}

def save_player_name(key):
    names_dict[key] = pyperclip.paste()

def capture_screenshot(y_position, count):
    pg.click(x=848, y=y_position, clicks=1, interval=0.8)

    pg.click(x=1175, y=435, clicks=1, interval=0.8) # move to ? and click
    pg.screenshot(f"{count}-kills.png")

    pg.click(x=409, y=766, clicks=1, interval=0.8) # move to more info and click
    pg.screenshot(f"{count}-detail.png")

    pg.click(x=397, y=225, clicks=1, interval=0.8) # copy player name to clipboard
    save_player_name(count) # save player name to dictionary

    pg.click(x=1464, y=116, clicks=1, interval=0.8) # move to X and click
  
    pg.click(x=1432, y=168, clicks=1, interval=0.8) # move to X and click

    pg.moveTo(848, y_position, 0.3) # move to the id

    
# Capture top 3
count = 1
top2_y = 365

pg.click(x=848, y=top2_y, clicks=1, interval=0.8)

while count <= 3:
    capture_screenshot(top2_y, count)
    count += 1
    top2_y += 100

# Capture the rest
UP_TO = 6
count = 4
y_position = 685
while count <= UP_TO:
    capture_screenshot(y_position, count)
    pg.drag(0, -100, 0.8, button = "left") # drag up

    y_position = 600
    count += 1

print(names_dict)