import cv2
import mediapipe as mp
import simpleaudio as sa
import pygame.midi
import time
import mido
import pygame
#=========================
#원래 있던 midi 파일 실행   play_music()
#=========================

do = sa.WaveObject.from_wave_file("sounds/1.wav")
re = sa.WaveObject.from_wave_file("sounds/2.wav")
mi = sa.WaveObject.from_wave_file("sounds/3.wav")
fa = sa.WaveObject.from_wave_file("sounds/4.wav")
sol = sa.WaveObject.from_wave_file("sounds/5.wav")


#midi filename생성 
midi_filename = []
notes = [60, 62, 64, 65, 67, 69, 71]
for i, note in enumerate(notes):    
    midi_filename.append(str(note) +'.mid')
    
    
# Initialize Pygame and the MIDI module
pygame.init()
pygame.midi.init()


def is_object_in_area(object_location, area):
    x, y = object_location
    start_x, start_y, width, height = area
    return start_x <= x < start_x + width and start_y <= y < start_y + height

# Mediapipe Hand Landmark 모델 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, 
                       max_num_hands=2, 
                       min_detection_confidence=0.7, 
                       min_tracking_confidence=0.7)



# 웹캠 초기화
cap = cv2.VideoCapture(0)
cnt=0

# 10개의 객체의 위치를 나타내는 리스트
object_locations = [(2, 4), (5, 3), (1, 2), (4, 1), (3, 5), (5, 2), (2, 3), (1, 5), (3, 1), (4, 4)]

# 5개의 영역을 나타내는 리스트, 각각의 영역은 (시작 x 좌표, 시작 y 좌표, 가로 길이, 세로 길이) 형태로 저장
areas = [(80, 300, 100, 60), (180, 300, 100, 60),(280, 300, 100, 60),(380, 300, 100, 60),(480, 300, 100, 60)]

prev_event = None
music_playing = False
flag = False
event = 0
while True:
    # 웹캠에서 프레임 읽기 & 좌우반전
    ret, frame = cap.read()
    result = cv2.flip(frame, 1) 

    # Mediapipe Hand Landmark 모델을 사용하여 이미지 처리
    image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # 각 손가락 끝의 랜드마크 좌표 추출
    fingertips = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for finger_tip_id in [4, 8, 12, 16, 20]:
                lm = handLms.landmark[finger_tip_id]
                h, w, c = result.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                fingertips.append((cx, cy))

        # 손가락 끝에 원 그리기
        for fingertip in fingertips:              
            cv2.circle(result, fingertip, 5, (255, 0, 0), -1)             

        # 손가락 끝 좌표가 각 영역 안에 포함되는지 확인하고 해당하는 이벤트 발생
        event = -1
        for location in fingertips:
            for i, area in enumerate(areas):
                if is_object_in_area(location, area):
                    cv2.putText(result, str(i), (100 + i * 50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    event = i
                    break

            if event != -1:
                break

        # 이전 이벤트와 다를 경우 소리 재생
        if event != -1 and event != prev_event:
            if event == 0:
                do.play()
            elif event == 1:
                re.play()
            elif event == 2:
                mi.play() 
            elif event == 3:
                fa.play()
            elif event == 4:
                sol.play()

    # 영역 표시 
    for i, area in enumerate(areas):
        cv2.rectangle(result,(area[0], area[1]),(area[0]+area[2], area[1]+area[3]),(0,0,255),2)  #레

    # 결과 보여주기
    cv2.imshow("Fingertip Detection division", result)

    # 'q' 키를 누르면 루프 탈출
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 해제 및 모든 윈도우 종료

pygame.midi.quit()
cap.release()
cv2.destroyAllWindows()

