import cv2
import os
from tkinter.filedialog import askopenfiles

# Read image
files = askopenfiles("r", filetypes=[('Image', '.jpg .png .bmp')], multiple=True)

for file in files:
    contractor = False
    customer = False

    img = cv2.imread(file.name)
    name, extension = os.path.splitext(file.name)
    try:
        resultText = open('result.txt', 'x')
    except OSError:
        resultText = open('result.txt', 'a')
    resultText.write(name + ':\n')

    hh, ww = img.shape[:2]
    # Convert to HSV and extract the saturation channel
    sat = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:, :, 1]
    # median filter
    median = cv2.medianBlur(sat, 7)
    # get Hough circles
    min_dist = ww // 20
    circles = cv2.HoughCircles(median, cv2.HOUGH_GRADIENT, 1, minDist=min_dist, param1=150,
                               param2=50, minRadius=0, maxRadius=0)

    resultImg = img.copy()
    for circle in circles[0]:
        (x, y, r) = circle
        x = int(x)
        y = int(y)
        r = int(r)
        if x < ww // 2:
            contractor = True
        else:
            customer = True
        cv2.circle(resultImg, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(resultImg, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    if contractor:
        resultText.write('Исполнитель - Да, ')
    else:
        resultText.write('Исполнитель - Нет, ')
    if customer:
        resultText.write('Заказчик - Да')
    else:
        resultText.write('Заказчик - Нет')
    resultText.write('\n')

    cv2.imwrite(name + '_redacted' + extension, resultImg)
