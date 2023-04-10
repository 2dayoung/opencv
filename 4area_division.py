#파란 원 영역에 들어오면 점수 + 트랙바 

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


# 파란색 범위 설정 (HSV)
# lower_blue = (100, 30, 30)
# upper_blue = (130, 255, 255)

# 웹캠 캡처 생성
cap = cv2.VideoCapture(0)


while True:
    # 현재 프레임 캡처
    ret, frame = cap.read()

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
    cv2.imshow("mask",mask)

    #잡음제거 
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    mask = closing

    # 파란색 영역 마스크 생성
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    #cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    #cv2.erode(mask,mask)
    cv2.imshow("open",mask)

    # 마스크에서 파란색 물체 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #두개만 추출
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    # 파란색 물체가 존재하면 점수 증가
    if len(contours) >= 2:
        # 파란색 원 중심 좌표 추출
        center_list = []
        for cnt in contours:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            if radius > 5:
                center_list.append((int(x), int(y)))
        #for center in center_list:
            #cv2.circle(result, center, int(radius), (0, 255, 0), 2)
        # 두 개의 원이 존재하면 각각 원으로 표시
        if len(center_list) > 2:
            for center in center_list:
                cv2.circle(frame, center, int(radius), (0, 255, 0), 2)

            # 왼쪽 하단 영역에 들어온 원이면 점수 증가
            if center_list[0][0] < 160 and center_list[0][1] > 360:
                cv2.putText(result, "Do", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if center_list[1][0] > 160 and center_list[1][0] < 320 and center_list[1][1] > 360:
                cv2.putText(result, "Re", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if center_list[1][0] > 320 and center_list[1][0] < 480 and center_list[1][1] > 360:
                cv2.putText(result, "Mi", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if center_list[1][0] > 480 and center_list[1][0] < 640 and center_list[1][1] > 360:
                cv2.putText(result, "Fa", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    # 영역 표시 
    cv2.rectangle(result,(0,360),(160,480),(0,0,255),2),  #도 
    cv2.rectangle(result,(160,360),(320,480),(54,148,255),2)  #레
    cv2.rectangle(result,(320,360),(480,480),(0,228,255),2)  #미
    cv2.rectangle(result,(480,360),(640,480),(22,219,29),2)  #파


    # 이미지 출력
    cv2.imshow("Webcam", result)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
