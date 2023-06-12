#파란 원 영역에 들어오면 점수 + 트랙바 

import cv2
import numpy as np
import simpleaudio as sa

# Initialize HSV values
h, s, v = 0, 0, 0

# 웹캠 캡처 생성
cap = cv2.VideoCapture(0)

# 트랙바를 위한 콜백 함수
def nothing(x):
    pass

# Initialize flag for drawing rectangle
draw_rectangle = False

def get_color(event, x, y, flags, param):
    global h, s, v, draw_rectangle  # Declare the variables as global
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Retrieve the color at the clicked point in BGR format
        color = frame[y, x]

        # Convert BGR to HSV format
        hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2HSV)

        # Retrieve the H, S, V values from HSV format
        h, s, v = hsv_color[0][0]

        print(f"Clicked color: BGR({color[2]}, {color[1]}, {color[0]}) | HSV({h}, {s}, {v})")
        
        # Set the flag to True for drawing the rectangle
        draw_rectangle = True
# 윈도우와 트랙바 생성
cv2.namedWindow('frame')
cv2.createTrackbar('low_H', 'frame', 0, 255, nothing)
cv2.createTrackbar('low_S', 'frame', 0, 255, nothing)
cv2.createTrackbar('low_V', 'frame', 0, 255, nothing)
cv2.createTrackbar('high_H', 'frame', 255, 255, nothing)
cv2.createTrackbar('high_S', 'frame', 255, 255, nothing)
cv2.createTrackbar('high_V', 'frame', 255, 255, nothing)


# 파란색 범위 설정 (HSV)
# lower_blue = (100, 30, 30)
# upper_blue = (130, 255, 255)



# Create a window and set the mouse event callback function
cv2.namedWindow("Webcam")
cv2.setMouseCallback("Webcam", get_color)

while True:
    # 현재 프레임 캡처
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imshow("Webcam", frame)

    # 프레임이 캡처되지 않았으면 종료
    if not ret:
        break

    # 이미지 크기 조정
    frame = cv2.resize(frame, (640, 480))

    #화면 반전
    result= cv2.flip(frame,1) 

    # 이미지를 BGR에서 HSV로 변환
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

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
    # cv2.imshow("mask",mask)

    # 잡음 제거를 위한 모폴로지 연산
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("closing ",closing )

    # 객체 검출
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 두 개의 가장 큰 객체만 추출
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    # 객체 위치 추출
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
          
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # 이미지 출력
    cv2.imshow("Webcam", result)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()





