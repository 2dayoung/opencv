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

    # 컨투어 중 가장 큰 영역을 찾습니다.
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        
        # 컨투어 내부에 파란색 원이 있는지 검사합니다.
        M = cv2.moments(max_contour)
        if M['m00'] != 0:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])
            
            # 컨투어를 둘러싸는 최소한의 사각형을 구합니다.
            x,y,w,h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            
            # 원을 그립니다.
            cv2.circle(frame, (x, y), 20, (0, 0, 255), 2)
            
            # 원이 가운데 영역에 위치한 경우 점수를 1 증가시킵니다.
            if (x-center_x)**2 + (y-center_y)**2 < radius**2:
                score += 1
        
    # 가운데 원을 그립니다.
    cv2.circle(frame, (center_x, center_y), radius, (255, 0, 0), 2)

    # 점수를 출력합니다.
    cv2.putText(frame, "Score: {}".format(score), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 결과를 출력합니다.
    cv2.imshow('frame', frame)

    # ESC 키를 누르면 종료합니다.
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
