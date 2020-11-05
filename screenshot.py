import pyautogui as pg
import os
import pyperclip


if not os.path.exists("player images"):
    os.makedirs("player images")

os.chdir("player images")


clipboard_data = pyperclip.paste()
print(clipboard_data)



# Capture top 3
count = 10
y_position = 365
pg.click(x=848, y=365, clicks=1, interval=0.8)
while count < 3:
    pg.click(x=848, y=y_position, clicks=1, interval=0.8)

    pg.click(x=1175, y=435, clicks=1, interval=0.8) # move to ? and click
    pg.screenshot(f"{count}-kills.png")

    pg.click(x=409, y=766, clicks=1, interval=0.8) # move to more info and click
    pg.screenshot(f"{count}-detail.png")

    pg.click(x=1464, y=116, clicks=1, interval=0.8) # move to X and click
  
    pg.click(x=1432, y=168, clicks=1, interval=0.8) # move to X and click

    pg.moveTo(848, 598, 0.3) # move to the id

    count += 1
    y_position += 100

# Capture the rest
UP_TO = 400
count = 3000
while count <= UP_TO:
    pg.click(x=848, y=595, clicks=1, interval=0.8) # move to governor and click

    pg.click(x=1175, y=435, clicks=1, interval=0.8) # move to ? and click
    pg.screenshot(f"{count}-kills.png")

    pg.click(x=409, y=766, clicks=1, interval=0.8) # move to more info and click
    pg.screenshot(f"{count}-detail.png")

    pg.click(x=1464, y=116, clicks=1, interval=0.8) # move to X and click
  
    pg.click(x=1432, y=168, clicks=1, interval=0.8) # move to X and click

    pg.moveTo(848, 595, 0.8) # move to the id
    pg.drag(0, -100, 0.8, button = "left") # drag up

    count += 1