import pyautogui as pg

count = 4
pg.click(x=848, y=598, clicks=1, interval=0.3)
while count < 7:
    pg.click(x=848, y=598, clicks=1, interval=0.5) # move to governor and click

    pg.click(x=1175, y=435, clicks=1, interval=0.5) # move to ? and click
    pg.screenshot(f"{count}-kills.png")

    pg.click(x=409, y=766, clicks=1, interval=0.5) # move to more info and click
    pg.screenshot(f"{count}-detail.png")

    pg.click(x=1464, y=116, clicks=1, interval=0.5) # move to X and click
  
    pg.click(x=1432, y=168, clicks=1, interval=0.5) # move to X and click

    pg.moveTo(848, 598, 0.3) # move to the id
    pg.drag(0, -100, 0.3, button = "left") # drag up
    count += 1