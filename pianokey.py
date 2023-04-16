import cv2
import numpy as np

cap = cv2.VideoCapture(0) # 노트북 내장 카메라 취득

while True:
    # 영상 취득
    ret, frame = cap.read()

    # 흑백 영상으로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 이진화
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 노이즈 제거
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    # 윤곽선 검출
    contours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 건반 영역 추출
    key_area = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h > 100 and w > 20:
            key_area.append([x, y, w, h])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 화면에 출력
    cv2.imshow('frame', frame)

    # 종료 조건
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 해제
cap.release()
cv2.destroyAllWindows()