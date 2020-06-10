import cv2, os
import numpy as np

os.system('cls')

print("\nНОВЫЙ ПОДСЧЕТ:")
img = cv2.imread ('./image.jpg', 0)
img = cv2.medianBlur (img, 5)
mask = np.zeros(img.shape, dtype=np.uint8)

# -------------- ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ -----------------

# MIN_SIZE = 100 # минимальный необходимый размер объекта для подсчета, все, что меньше, - шум (100)
kernel = np.ones((10,10),np.uint8) # выстраивание контура по пороговым значениям (10, 10)
opening = cv2.erode(img, kernel, iterations = 3) # эрозия объекта, размытие внешних частей (iterations = 3)

# ----------- КОНЕЦ ИЗМЕНЯЕМЫХ ПАРАМЕТРОВ -------------

cnts = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# поиск max_area
max_area = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > max_area:
        max_area = area
print("Максимальный размер объекта", max_area)

MIN_SIZE = (max_area/100) * 4 # 4% - минимальный размер необходимого объекта
print("Минимальный размер объекта", MIN_SIZE)

blobs = 0
count = 0
i = 0

for c in cnts:
    i += 1
    area = cv2.contourArea(c)
    cv2.drawContours(mask, [c], -1, (36,255,12), -1)

    if area > MIN_SIZE:
        count = 1
    else:
        count = 0

    stri = str(i)
    stri += ")"
    if (i < 10) and (area < 10):
        print(stri, area, "\t\tЧисло сфер:", count)
    else:
        print(stri, area, "\tЧисло сфер:", count)

    blobs += count

print('\nОбщее число сфер:', blobs, "\n")

mask = cv2.resize(mask, (960, 540))
cv2.imshow('mask', mask)

cv2.waitKey()