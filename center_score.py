#가운데 원에 들어오면 점수

import cv2
import numpy as np

# 트랙바를 위한 콜백 함수
def nothing(x):
    pass

# 웹캠에서 프레임을 캡처합니다.
cap = cv2.VideoCapture(0)

# 윈도우와 트랙바 생성
cv2.namedWindow('frame')
cv2.createTrackbar('low_H', 'frame', 0, 255, nothing)
cv2.createTrackbar('low_S', 'frame', 0, 255, nothing)
cv2.createTrackbar('low_V', 'frame', 0, 255, nothing)
cv2.createTrackbar('high_H', 'frame', 255, 255, nothing)
cv2.createTrackbar('high_S', 'frame', 255, 255, nothing)
cv2.createTrackbar('high_V', 'frame', 255, 255, nothing)

# 가운데 원을 그리기 위한 변수
center_x = 320
center_y = 240
radius = 50
score = 0

while True:
    # 프레임을 읽어옵니다.
    ret, frame = cap.read()
    
    # BGR 이미지를 HSV 이미지로 변환합니다.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 트랙바 값으로 색상 범위를 설정합니다.
    low_H = cv2.getTrackbarPos('low_H', 'frame')
    low_S = cv2.getTrackbarPos('low_S', 'frame')
    low_V = cv2.getTrackbarPos('low_V', 'frame')
    high_H = cv2.getTrackbarPos('high_H', 'frame')
    high_S = cv2.getTrackbarPos('high_S', 'frame')
    high_V = cv2.getTrackbarPos('high_V', 'frame')
    lower_color = np.array([low_H, low_S, low_V])
    upper_color = np.array([high_H, high_S, high_V])
    
    # HSV 이미지에서 색상 범위에 해당하는 영역을 이진화합니다.
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # 컨투어를 찾습니다.
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 컨투어 중에서 파란색 원에 해당하는 원을 찾습니다.
    blue_circles = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
        # 컨투어를 감싸는 최소한의 원을 구합니다.
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
                    # 파란색 원이라면 원 중심과 가운데 원의 거리를 구합니다.
            if 110 <= hsv[int(y), int(x), 0] <= 130:
                blue_circles.append((center, radius))
                distance = np.sqrt((center_x - center[0]) ** 2 + (center_y - center[1]) ** 2)
                
                # 파란색 원과 가운데 원의 거리가 가운데 원의 반지름보다 작다면 점수를 1 증가시킵니다.
                if distance < radius:
                    score += 1

    # 파란색 원을 원본 이미지에 그립니다.
    for circle in blue_circles:
        center, radius = circle
        cv2.circle(frame, center, radius, (255, 0, 0), 3)

    # 가운데 원을 원본 이미지에 그립니다.
    cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 3)

    # 현재 점수를 화면에 출력합니다.
    cv2.putText(frame, 'Score: {}'.format(score), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # 결과를 보여줍니다.
    cv2.imshow('frame', frame)

    # ESC 키를 누르면 종료합니다.
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()