import re
import cv2
import pytesseract
from pytesseract import Output
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def enhance_Image(image):
    # Grayscale, Gaussian blur, Otsu's threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    return thresh
    
def remove_noise_and_smooth(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 41)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    or_image = cv2.bitwise_or(img, closing)
    return or_image

# [y1:y2, x1:x2]
# udi [280:320, 929:1095]
# alliance [434:475 , 770:1085]
# kills [548:710, 1140:1545]
# t4 [612:647, 1377:1542]
# t5 [662:694, 1195:1360]
# total kills [457:486, 1250:1395]

# 2nd picture
# copy name (451, 184)
# power [154:214 , 874:1162]
# dead [533:593 ,1387:1587]


img = cv2.imread("Capture.PNG")
img = img[457:486, 1250:1395]
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(img,(5,5),0)
# img = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
# kernel = np.ones((3,3),np.uint8)
# img = cv2.erode(img,kernel,iterations = 1)

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
