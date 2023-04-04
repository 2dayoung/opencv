import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# 원의 중심 좌표와 반지름 범위를 설정합니다.
blue_lower = np.array([100, 50, 50])
blue_upper = np.array([130, 255, 255])
center_x = 320
center_y = 240
radius = 100

# 점수 변수를 초기화합니다.
score = 0

while True:
    ret, frame = cap.read()

    # 원 검출을 위해 BGR 이미지를 HSV로 변환합니다.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 파란색 원을 검출합니다.
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 원이 검출되면 가장 큰 원을 찾습니다.
    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(cnt)
        
        # 원이 가운데 영역에 위치한 경우 점수를 1 증가시킵니다.
        if (x-center_x)**2 + (y-center_y)**2 < radius**2:
            score += 1

        # 원을 그리고, 중심점을 표시합니다.
        cv2.circle(frame, (int(x), int(y)), int(r), (0, 255, 0), 2)
        cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)

    # 현재 점수를 화면에 출력합니다.
    cv2.putText(frame, "Score: {}".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
