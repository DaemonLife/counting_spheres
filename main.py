import cv2
import numpy as np

# from matplotlib import pyplot as plt

SIZE = 6300

print("\n")

img = cv2.imread ('image.jpg', 0)
img = cv2.medianBlur (img, 5)
mask = np.zeros(img.shape, dtype=np.uint8)

ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
# titles = ['Original Image', 'Global Thresholding (v = 127)',
#             'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [img, th1, th2, th3]
# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()

kernel = np.ones((0,0),np.uint8)
opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel, iterations=8)
cnts = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if len(cnts) == 2 else cnts[1]

blobs = 0
i = 0
count = 0
for c in cnts:
    i += 1
    area = cv2.contourArea(c)
    cv2.drawContours(mask, [c], -1, (36,255,12), -1)

    stri = str(i)
    stri += ")"
    print(stri, area)
    count = (area/SIZE)
    count = round(count)

    print("Число сфер:", count)
    blobs += count

print('\nОбщее число сфер:', blobs)


mask = cv2.resize(mask, (960, 540))
cv2.imshow('mask', mask)

cv2.waitKey()