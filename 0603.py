import cv2
import numpy as np

# 마우스 이벤트 콜백 함수
def mouse_callback(event, x, y, flags, param):
    global roi_points, mouse_click_count

    if event == cv2.EVENT_LBUTTONDOWN:
        if mouse_click_count < 4:
            roi_points.append((x, y))
            mouse_click_count += 1

        
# roi 변수 초기화
roi_points = []
mouse_click_count = 0
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
    frame = cv2.resize(frame, None, fx=1.5, fy=1.5)

    # 마우스 드래그 영역 표시
    # if mouse_drag_started:
    #     cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (255, 0, 0), 2)
    # ROI 영역 그리기
    for i in range(len(roi_points)):
        cv2.circle(frame, roi_points[i], 5, (0, 0, 255), -1)

    # 결과 출력
    cv2.imshow("Camera", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q') or mouse_click_count >= 4:
        break

# 마우스 드래그가 시작되면 영역 추출을 위한 변수 설정
if len(roi_points) == 4:
    image = frame.copy()

# 건반 영역을 나타내는 4개의 점을 정렬
    roi_points = sorted(roi_points, key=lambda x: x[1])

    # 사다리꼴을 형성하기 위한 좌표 계산
    top_left = roi_points[0]
    top_right = roi_points[1]
    bottom_right = roi_points[2]
    bottom_left = roi_points[3]
    roi_x = top_left
    roi_y = top_right


    # 사다리꼴 좌표
    src_points = np.float32([top_left, top_right, bottom_right, bottom_left])

    # 변환된 사다리꼴의 폭과 높이 계산
    width_top = np.linalg.norm(np.array(top_right) - np.array(top_left))
    width_bottom = np.linalg.norm(np.array(bottom_right) - np.array(bottom_left))
    height_left = np.linalg.norm(np.array(bottom_left) - np.array(top_left))
    height_right = np.linalg.norm(np.array(bottom_right) - np.array(top_right))

    # 변환된 사다리꼴의 폭과 높이 중 최댓값을 적용하여 결과 이미지 크기 계산
    max_width = max(int(width_top), int(width_bottom))
    max_height = max(int(height_left), int(height_right))

    # 결과 이미지 좌표
    dst_points = np.float32([[0, 0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]])

    # Perspective Transform 행렬 계산
    transform_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Perspective Transform 적용
    result_image = cv2.warpPerspective(image, transform_matrix, (max_width, max_height))

    frame = result_image
    cv2.imshow("result_image",frame)
    cv2.waitKey(0)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 영역 추출을 위한 ROI 설정
    roi = frame[roi_y:roi_y + max_height, roi_x:roi_x + max_width]
    hsv_roi = hsv[roi_y:roi_y + max_height, roi_x:roi_x + max_width]

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

    frame[roi_y:roi_y + max_height, roi_x:roi_x + max_width] = roi
    cv2.imshow("Roi", result_image)
    cv2.waitKey(0)

# 카메라 객체와 창 해제
cap.release()
cv2.destroyAllWindows()