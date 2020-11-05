from PIL import Image, ImageEnhance, ImageFilter
import pytesseract as pt
import cv2
import xlsxwriter
from datetime import datetime
import os

# Create folder names folder if not exists
if not os.path.exists("names"):
    os.makedirs("names")

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

PLAYER_COUNT = 300
counter = 1
data = [] # array of dictionaries (data_dict)
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
    try:
        start_index = alliance.index('[')
    except:
        try:
            start_index = alliance.index('(')
        except:
            pass

    end_index = alliance.find(']')
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

    # Name (Does not work well with multiple languages, going to save the image itself)
    name_image  = enhance_Image(detail_image[400:500, 815:1530])
    custom_config = r'-l eng+kor+jap --psm 6'
    name = pt.image_to_string(name_image, config=custom_config)
    name = name.rstrip()
    print(f"name: {name}")
    data_dict["name"] = name
    # Save seperate name image to write to xlsx file
    os.chdir("names")
    cv2.imwrite(f"{counter}-name.png", name_image)
    data_dict["name_image"] = f"{counter}-name.png"
    os.chdir("..")

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

    # Resource Assistance
    rss = ""
    rss_x = 2375
    while not rss.isdigit():
        rss = image_to_string(detail_image, 1565, 1640, rss_x, 2740)
        rss = rss.replace(",", "")
        try:
            int(rss)
        except:
            rss_x += 2
        if rss_x > 2650:
            break

    print(f"rss: {rss}")
    data_dict["rss"] = rss

    counter += 1
    data.append(data_dict)

# write to xlsx
workbook = xlsxwriter.Workbook("Detailed Player info.xlsx")
worksheet = workbook.add_worksheet()

bold = workbook.add_format({"bold":True})

now = datetime.now()
current_date_time = now.strftime("%d/%m/%Y %H:%M")

worksheet.write("A1", "Created On:", bold)
worksheet.write("B1", f"{current_date_time}", bold)

worksheet.write("A2", "Name", bold)
worksheet.write("B2", "UID", bold)
worksheet.write("C2", "Alliance", bold)
worksheet.write("D2", "Power", bold)
worksheet.write("E2", "Total Kills", bold)
worksheet.write("F2", "T4 Kills", bold)
worksheet.write("G2", "T5 Kills", bold)
worksheet.write("H2", "Dead", bold)
worksheet.write("I2", "Rss Assist", bold)
worksheet.write("J2", "Name Image", bold)

row_num = 3
for player_dict in data:
    worksheet.write(f"A{row_num}", player_dict["name"])
    worksheet.write(f"B{row_num}", player_dict["id"])
    worksheet.write(f"C{row_num}", player_dict["alliance"])
    worksheet.write(f"D{row_num}", player_dict["power"])
    worksheet.write(f"E{row_num}", player_dict["total_kills"])
    worksheet.write(f"F{row_num}", player_dict["t4_kills"])
    worksheet.write(f"G{row_num}", player_dict["t5_kills"])
    worksheet.write(f"H{row_num}", player_dict["dead"])
    worksheet.write(f"I{row_num}", player_dict["rss"])
    worksheet.insert_image(f"J{row_num}", "names/"+player_dict["name_image"], {"x_scale":0.2, "y_scale":0.2})
    row_num += 1

workbook.close()

# image  = enhance_Image(detail_image[1565:1640, 2375:2740])
# cv2.imshow("image", image)
# cv2.waitKey(0)



