import cv2

# 파란색 범위 설정 (HSV)
lower_blue = (100, 50, 50)
upper_blue = (130, 255, 255)

# 웹캠 캡처 생성
cap = cv2.VideoCapture(0)

# 점수 초기화
score = 0

while True:
    # 현재 프레임 캡처
    ret, frame = cap.read()

    # 프레임이 캡처되지 않았으면 종료
    if not ret:
        break

    # 이미지 크기 조정
    frame = cv2.resize(frame, (640, 480))

    # 이미지를 BGR에서 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 파란색 영역 마스크 생성
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 마스크에서 파란색 물체 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 파란색 물체가 존재하면 점수 증가
    if len(contours) >= 2:
        # 파란색 원 중심 좌표 추출
        center_list = []
        for cnt in contours:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            if radius > 10:
                center_list.append((int(x), int(y)))

        # 두 개의 원이 존재하면 각각 원으로 표시
        if len(center_list) == 2:
            for center in center_list:
                cv2.circle(frame, center, int(radius), (0, 255, 0), 2)

            # 왼쪽 하단 영역에 들어온 원이면 점수 증가
            if center_list[0][0] < 320 and center_list[0][1] > 360:
                score += 1
            if center_list[1][0] < 320 and center_list[1][1] > 360:
                score += 1

    # 점수를 이미지에 출력
    cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    # 이미지 출력
    cv2.imshow("Webcam", frame)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
