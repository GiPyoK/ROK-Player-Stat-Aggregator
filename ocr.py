from PIL import Image, ImageEnhance, ImageFilter
import pytesseract as pt
import cv2

def enhance_Image(image):
    # Grayscale, Gaussian blur, Otsu's threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    return invert

def image_to_string(input_image, y1, y2, x1, x2):
    image  = enhance_Image(input_image[y1:y2, x1:x2])
    ocr_string = pt.image_to_string(image)
    ocr_string = ocr_string.strip()
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    return ocr_string

kill_image = cv2.imread("5-kills.png")

# Player ID
player_id_x = 1830
player_id = ""
while not player_id.isdigit():
    player_id = image_to_string(kill_image, 610, 690, 1630, player_id_x)
    # remove ')' from the end of the string
    try:
        int(player_id[-1])
    except:
        player_id = player_id[0:-1]

    player_id_x += 5
    if player_id_x - 1630 > 500:
        break

print(player_id)

# Alliance
alliance = image_to_string(kill_image, 888, 970, 1333,1900) #sample output: "(HOF]Hall of Fame"
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
print(alliance)


# Total kills
total_kills = image_to_string(kill_image, 935, 985, 2185, 2385)
total_kills = total_kills.strip(",")
print(total_kills)
print(total_kills.isdigit())
# image  = enhance_Image(kill_image[935:985, 2185:2385])
# cv2.imshow("image", image)
# cv2.waitKey(0)


