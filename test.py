import cv2
import numpy as np

# 마우스 이벤트 콜백 함수
def mouse_callback(event, x, y, flags, param):
    global roi_points, mouse_click_count

    if event == cv2.EVENT_LBUTTONDOWN:
        if mouse_click_count < 4:
            roi_points.append((x, y))
            mouse_click_count += 1


# 건반 영역 변수 초기화
roi_points = []
mouse_click_count = 0

# 건반 사진 불러오기
image = cv2.imread("piano_image.jpg")

# 건반 영역 선택을 위한 창 생성
cv2.namedWindow("Piano")
cv2.setMouseCallback("Piano", mouse_callback)

while True:
    # 건반 영역 그리기
    for i in range(len(roi_points)):
        cv2.circle(image, roi_points[i], 5, (0, 0, 255), -1)

    # 이미지 출력
    cv2.imshow("Piano", image)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q') or mouse_click_count >= 4:
        break

# 건반 영역을 나타내는 4개의 점을 정렬
roi_points = sorted(roi_points, key=lambda x: x[1])

# 사다리꼴을 형성하기 위한 좌표 계산
top_left = roi_points[0]
top_right = roi_points[1]
bottom_right = roi_points[2]
bottom_left = roi_points[3]

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

# 결과 출력
cv2.imshow("Piano ROI", result_image)
cv2.waitKey(0)

# 종료
cv2.destroyAllWindows()
