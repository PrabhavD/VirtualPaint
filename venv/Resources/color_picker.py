#use numpy 1.19.3 as 1.19.4 is incompatible as of Dec 31, 2020
import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth) #width id no. 3
cap.set(4, frameHeight) #height id no. 4
cap.set(10, 150) #brightness id no. 10

def empty(x):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
#.createTrackbar params: (title, window, initial value, max value, function)
cv2.createTrackbar("HUE_MIN", "HSV", 0, 179, empty)
cv2.createTrackbar("SAT_MIN", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE_MIN", "HSV", 0, 255, empty)
cv2.createTrackbar("HUE_MAX", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT_MAX", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE_MAX", "HSV", 255, 255, empty)

while True:

    _, img = cap.read()

    #convert image to HSV (hue, saturation, value)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE_MIN", "HSV")
    h_max = cv2.getTrackbarPos("HUE_MAX", "HSV")
    s_min = cv2.getTrackbarPos("SAT_MIN", "HSV")
    s_max = cv2.getTrackbarPos("SAT_MAX", "HSV")
    v_min = cv2.getTrackbarPos("VALUE_MIN", "HSV")
    v_max = cv2.getTrackbarPos("VALUE_MAX", "HSV")
    print(h_min, h_max, s_min, s_max, v_min, v_max)

    #create mask to give filtered out image using min/max colors
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)

    #new image created from HSV outline
    #.bitwise_and creates image fron common pixels of both
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, imgResult])
    # cv2.imshow("Original", img)
    # cv2.imshow("HSV Color", imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Result", imgResult)
    cv2.imshow("Horizontal Stacking", hStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
#cv2.destroyAllWindows()