import cv2 as cv
import numpy as np

# Haar Cascade 분류기 로드
finger_cascade = cv.CascadeClassifier('hand.xml')
# 웹캠 연결
cap = cv.VideoCapture(0)

while True:
    # 프레임 받아오기
    ret, frame = cap.read()
    
    # 그레이스케일로 변환
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # 손가락 끝 검출
    fingers = finger_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 검출된 손가락 끝 좌표 출력
    for (x, y, w, h) in fingers:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 결과 출력
    cv.imshow("Finger detection", frame)
    
    # 종료를 위한 키 입력 대기
    key = cv.waitKey(1)
    if key == 27: # ESC 키 입력 시 종료
        break

# 자원 반환
cap.release()
cv.destroyAllWindows()

