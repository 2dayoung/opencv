import cv2
#0이면 노트북 내장 웹캠 숫자를 올리면 추가된 웹캠을 이용할 수 있다.
cap = cv2.VideoCapture(0)
# 3은 가로 4는 세로 길이 
cap.set(3, 720)
cap.set(4, 1080)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    cv2.imshow('test', frame)

    k = cv2.waitKey(1)
    if cv2.waitKey(1) != -1:
        break

cap.release()

cv2.destroyAllWindows()