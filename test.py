import re
import cv2
import pytesseract
from pytesseract import Output
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def enhance_Image(image):
    # Grayscale, Gaussian blur, Otsu's threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    return opening

def enhance_Image2(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(image,(5,5),0)
    image = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    kernel = np.ones((2,2),np.uint8)
    image = cv2.erode(image,kernel,iterations = 1)
    return image    

def remove_noise_and_smooth(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered = cv2.adaptiveThreshold(image.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 41)
    kernel = np.ones((111, 111), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    or_image = cv2.bitwise_or(image, closing)
    return or_image

# [y1:y2, x1:x2]
# udi [280:320, 935:1095]
# alliance [434:475 , 770:921]
# t4 [868:918, 1504:1713]
# t5 [922:972, 1504:1713]

# 2nd picture
# copy name (451, 184)
# power [154:214 , 874:1162]
# dead troops [533:593 ,1387:1587]


img = cv2.imread("2-kills.PNG")
img = img[280:320, 935:1095]
# img = enhance_Image(img)
# img = enhance_Image2(img)
# img = remove_noise_and_smooth(img)

# Perform OCR and save in data
data = pytesseract.image_to_data(img, output_type=Output.DICT)
# draw boxes around each data
n_boxes = len(data['level'])
for i in range(n_boxes):
    (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

print(data["text"])
print("".join(data["text"]))

cv2.imshow('img', img)
cv2.waitKey(0)
