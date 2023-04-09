import cv2
import numpy as np
import simpleaudio as sa

# 특정 영역과 실행할 wav 파일을 딕셔너리로 저장
objects = {"area1": "1.wav",
           "area2": "2.wav",
           "area3": "3.wav",
           "area4": "4.wav"}

# wav 파일 로드
sounds = {obj: sa.WaveObject.from_wave_file(snd) for obj, snd in objects.items()}

# 동영상 파일 읽기
cap = cv2.VideoCapture('video.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    # 영상에서 객체를 감지하여 objects 딕셔너리의 키 값과 일치할 때 wav 파일 실행
    for obj, snd in sounds.items():
        # 객체가 감지된 영역 설정 (여기서는 임의로 사각형 영역 지정)
        x1, y1, x2, y2 = 100, 100, 200, 200
        area = frame[y1:y2, x1:x2]

        # 객체 감지
        # TODO: 객체 감지 코드 추가 (예를 들어, OpenCV의 CascadeClassifier 사용)

        # 객체가 감지된 경우 해당 객체의 키 값과 일치하는 경우 wav 파일 실행
        if obj_detected:
            snd.play()

    # 화면에 출력
    cv2.imshow('frame', frame)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



