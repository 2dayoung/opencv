import cv2
import numpy as np

#0이면 노트북 내장 웹캠 숫자를 올리면 추가된 웹캠을 이용할 수 있다.
cap = cv2.VideoCapture(0)
# 3은 가로 4는 세로 길이 
cap.set(3, 720)
cap.set(4, 1080)

while True:
    ret, frame = cap.read()
    frame1 = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(frame.shape, np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 2)
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
    cv2.imshow('output', drawing)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()