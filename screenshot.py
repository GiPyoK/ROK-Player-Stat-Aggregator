import pyautogui as pg
import os
import pyperclip
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract as pt
import cv2
from datetime import datetime
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from openpyxl import load_workbook

# Create header
XLSX_NAME = "Detailed Player info before kvk.xlsx"
WORKSHEET_NAME = "Player Info"

workbook = Workbook()
worksheet = workbook.active
worksheet.title = WORKSHEET_NAME

now = datetime.now()
current_date_time = now.strftime("%d/%m/%Y %H:%M")

worksheet["A1"] = "Created On:"
worksheet["B1"] = f"{current_date_time}"

worksheet["A2"] = "Rank"
worksheet["B2"] = "Name"
worksheet["C2"] = "UID"
worksheet["D2"] = "Alliance"
worksheet["E2"] = "Power"
worksheet["F2"] = "Total Kills"
worksheet["G2"] = "T4 Kills"
worksheet["H2"] = "T5 Kills"
worksheet["I2"] = "Dead"

workbook.save(filename = XLSX_NAME)

# Create player images folder if not exists
if not os.path.exists("player images"):
    os.makedirs("player images")


names_dict = {}

def save_player_name(rank):
    wb = load_workbook(filename = XLSX_NAME)
    ws = wb[WORKSHEET_NAME]
    row_num = rank+2

    ws[f"A{row_num}"] = rank
    ws[f"B{row_num}"] = pyperclip.paste()

    wb.save(XLSX_NAME)

def capture_screenshot(y_position, count):
    os.chdir("player images")
    
    pg.click(x=848, y=y_position, clicks=1, interval=2)

    pg.click(x=1175, y=435, clicks=1, interval=2) # move to ? and click
    pg.screenshot(f"{count}-kills.png")

    pg.click(x=409, y=766, clicks=1, interval=2) # move to more info and click
    pg.screenshot(f"{count}-detail.png")

    os.chdir("..") # Move back to root folder

    pg.click(x=397, y=225, clicks=1, interval=2) # copy player name to clipboard
    save_player_name(count) # save player name to dictionary

    pg.click(x=1464, y=116, clicks=1, interval=2) # move to X and click
  
    pg.click(x=1432, y=168, clicks=1, interval=2) # move to X and click

    pg.moveTo(848, y_position, 2) # move to the id


############ Screenshot ############
    
# Capture top 3
count = 1
top2_y = 365

pg.click(x=848, y=top2_y, clicks=1, interval=0.8)

while count <= 3:
    capture_screenshot(top2_y, count)
    count += 1
    top2_y += 100

# Capture the rest
UP_TO = 400
count = 4
y_position = 685
while count <= UP_TO:
    capture_screenshot(y_position, count)
    # pg.drag(0, -100, 0.8, button = "left") # drag up

    y_position = 708
    count += 1


############ OCR ############



def enhance_Image(image):
    # Grayscale, Gaussian blur, Otsu's threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # invert = 255 - opening
    return thresh

def image_to_string(input_image, y1, y2, x1, x2):
    image  = enhance_Image(input_image[y1:y2, x1:x2])
    ocr_string = pt.image_to_string(image)
    ocr_string = ocr_string.strip()
    # cv2.imshow("image", image)
    # print(ocr_string)
    # cv2.waitKey(0)
    return ocr_string

def write_to_xlsx(rank, data):
    wb = load_workbook(filename = XLSX_NAME)
    ws = wb[WORKSHEET_NAME]
    row_num = rank+2

    ws[f"C{row_num}"] = data["id"]
    ws[f"D{row_num}"] = data["alliance"]
    ws[f"E{row_num}"] = data["power"]
    ws[f"F{row_num}"] = data["total_kills"]
    ws[f"G{row_num}"] = data["t4_kills"]
    ws[f"H{row_num}"] = data["t5_kills"]
    ws[f"I{row_num}"] = data["dead"]

    wb.save(XLSX_NAME)





PLAYER_COUNT = 300
counter = 1
# data = [] # array of dictionaries (data_dict)
while counter <= PLAYER_COUNT:
    data_dict = {}

    kill_image = cv2.imread(f"player images/{counter}-kills.png")

    # Player ID
    player_id_x = 1930
    player_id = ""
    while not player_id.isdigit():
        player_id = image_to_string(kill_image, 610, 690, 1635, player_id_x)
        if player_id.isdigit():
            break
        # remove ')' from the end of the string
        try:
            int(player_id[-1])
        except:
            player_id = player_id[0:-1]

        player_id_x -= 2
        if player_id_x < 1640:
            break

    print(f"id: {player_id}")
    data_dict["id"] = player_id

    # Alliance
    alliance = image_to_string(kill_image, 888, 970, 1333,1550) #sample output: "(HOF]Hall of Fame"
    start_index = -1
    end_index = -1
    try:
        start_index = alliance.index('[')
    except:
        try:
            start_index = alliance.index('(')
        except:
            pass
    
    try:
        end_index = alliance.index(']')
    except:
        try:
            end_index = alliance.index(')')
        except:
            pass

    if start_index >= 0 and end_index > 0:
        alliance = alliance[start_index+1:end_index]
    print(f"alliance: {alliance}")
    data_dict["alliance"] = alliance


    # Total kills
    total_kills = ""
    total_kills_x = 2435
    while not total_kills.isdigit():
        total_kills = image_to_string(kill_image, 935, 985, 2185, total_kills_x)
        total_kills = total_kills.replace(",", "")
        try:
            int(total_kills)
        except:
            total_kills_x -= 2
        if total_kills_x < 2250:
            break

    print(f"total kills: {total_kills}")
    data_dict["total_kills"] = total_kills

    # T4 Kills
    t4_kills = ""
    t4_kills_x = 2685
    while not t4_kills.isdigit():
        t4_kills = image_to_string(kill_image, 1200, 1270, 2410, t4_kills_x)
        t4_kills = t4_kills.replace(",", "")
        try:
            int(t4_kills)
        except:
            t4_kills_x -= 2
        
        if t4_kills_x < 2460:
            break
    print(f"t4 kills: {t4_kills}")
    data_dict["t4_kills"] = t4_kills

    # T5 Kills
    t5_kills = ""
    t5_kills_x = 2340
    while not t5_kills.isdigit():
        t5_kills = image_to_string(kill_image, 1285, 1360, 2090, t5_kills_x)
        t5_kills = t5_kills.replace(",", "")
        try:
            int(t5_kills)
        except:
            t5_kills_x -= 2
        
        if t5_kills_x < 2150:
            break
        
    print(f"t5 kills: {t5_kills}")
    data_dict["t5_kills"] = t5_kills

    
    ##########################################

    detail_image = cv2.imread(f"player images/{counter}-detail.png")

    # Power
    power = ""
    power_x = 2000
    while not power.isdigit():
        power = image_to_string(detail_image, 415, 485, 1710, power_x)
        power = power.replace(",", "")
        try:
            int(power)
        except:
            power_x -= 2
        if power_x < 1770:
            break

    print(f"power: {power}")
    data_dict["power"] = power

    # Dead
    dead = ""
    dead_x = 2400
    while not dead.isdigit():
        dead = image_to_string(detail_image, 1070, 1140, dead_x, 2740)
        dead = dead.replace(",", "")
        try:
            int(dead)
        except:
            dead_x += 2
        if dead_x > 2680:
            break

    print(f"dead: {dead}")
    data_dict["dead"] = dead

    # # Resource Assistance
    # rss = ""
    # rss_x = 2375
    # while not rss.isdigit():
    #     rss = image_to_string(detail_image, 1565, 1640, rss_x, 2740)
    #     rss = rss.replace(",", "")
    #     try:
    #         int(rss)
    #     except:
    #         rss_x += 2
    #     if rss_x > 2650:
    #         break

    # print(f"rss: {rss}")
    # data_dict["rss"] = rss

    # data.append(data_dict)
    write_to_xlsx(counter, data_dict)
    counter += 1


# image  = enhance_Image(detail_image[1565:1640, 2375:2740])
# cv2.imshow("image", image)
# cv2.waitKey(0)



