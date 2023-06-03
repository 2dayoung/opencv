import cv2
import numpy as np

# 마우스 이벤트 콜백 함수
def mouse_callback(event, x, y, flags, param):
    global roi_x, roi_y, roi_width, roi_height, mouse_drag_started

    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_LBUTTONUP:
        roi_x, roi_y = x, y
        mouse_drag_started = True
        
# roi 변수 초기화
roi_x = 0
roi_y = 0
roi_width = 200
roi_height = 300
mouse_drag_started = False

# 카메라 캡처 객체 생성
cap = cv2.VideoCapture(0)

# 마우스 이벤트 콜백 등록
cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", mouse_callback)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 프레임 크기 조정 (선택 사항)
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

    # 마우스 드래그 영역 표시
    if mouse_drag_started:
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (255, 0, 0), 2)

    # 결과 출력
    cv2.imshow("Camera", frame)

    # 마우스 드래그가 시작되면 영역 추출을 위한 변수 설정
    if mouse_drag_started:
        # 프레임을 HSV 색 공간으로 변환
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 영역 추출을 위한 ROI 설정
        roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
        hsv_roi = hsv[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # 흰 건반과 검은 건반의 색상 범위 정의 (적절한 범위를 찾아 조정해야 할 수 있습니다)
        lower_white = np.array([0, 0, 200], dtype=np.uint8)
        upper_white = np.array([180, 30, 255], dtype=np.uint8)
        lower_black = np.array([0, 0, 0], dtype=np.uint8)
        upper_black = np.array([100, 50, 180], dtype=np.uint8)

        # 흰 건반 영역 추출
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        white_mask = cv2.inRange(hsv_roi, lower_white, upper_white)
        white_key_regions = cv2.bitwise_and(roi, roi, mask=white_mask)

        # 검은 건반 영역 추출
        black_mask = cv2.inRange(hsv_roi, lower_black, upper_black)
        black_key_regions = cv2.bitwise_and(roi, roi, mask=black_mask)

        # 흰 건반 영역 넘버링
        white_key_cnt = 1
        white_key_coords = []  

        for contour in cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                white_key_coords.append(x)  

        white_key_coords.sort()

        for x in white_key_coords:
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(roi, str(white_key_cnt), (x + int(w / 2) - 10, y + int(h / 2) + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            white_key_cnt += 1

        # 검은 건반 영역 넘버링
        black_key_cnt = 1
        black_key_coords = []  

        for contour in cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                black_key_coords.append(x)  

    
        black_key_coords.sort()

        for x in black_key_coords:
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(roi, str(black_key_cnt), (x + int(w / 2) - 10, y + int(h / 2) + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            black_key_cnt += 1

        # 결과 출력
        frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width] = roi

    cv2.imshow("Camera", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 's' 키를 누르면 roi_width와 roi_height 수정
    if cv2.waitKey(1) & 0xFF == ord('s'):
        roi_width = int(input("Enter new roi_width: "))
        roi_height = int(input("Enter new roi_height: "))

# 카메라 객체와 창 해제
cap.release()
cv2.destroyAllWindows()