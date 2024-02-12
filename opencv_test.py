import cv2
import numpy as np
def mask(i):
    img = cv2.imread(f'images/{i}.jpeg')
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    ORANGE_MIN_A = np.array([0, 150, 150],np.uint8)
    ORANGE_MAX_A = np.array([30, 255, 255],np.uint8)
    ORANGE_MIN_B = np.array([150, 100, 70],np.uint8)
    ORANGE_MAX_B = np.array([179, 255, 205],np.uint8)
    frame_threshed = cv2.bitwise_or(cv2.inRange(hsv_img, ORANGE_MIN_A,ORANGE_MAX_A),cv2.inRange(hsv_img, ORANGE_MIN_B, ORANGE_MAX_B))
    contours, _ = cv2.findContours(cv2.threshold(frame_threshed, 40, 255, 0)[1],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv2.contourArea)
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    print((cX, cY))
    cv2.drawContours(img,contours,-1,(0,255,0),3)
    img = cv2.circle(img, (cX, cY), 50, (0, 0, 255), -1)
    cv2.imwrite(f'out/{i}.png',img)
    cv2.imwrite(f'out/{i}mask.png',cv2.bitwise_and(cv2.cvtColor(hsv_img,cv2.COLOR_HSV2BGR),cv2.cvtColor(hsv_img,cv2.COLOR_HSV2BGR),mask=frame_threshed))
[mask(i) for i in range(1,10)]