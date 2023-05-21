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


#중복에 대해 진지하게 고민 

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
arr_prev_event = None
music_playing = False
flag = False
event = 0
arr_event = []
cnt = 0
while True:
    # 웹캠에서 프레임 읽기& 좌우반전 &크기
    ret, frame = cap.read()
    result= cv2.flip(frame,1) 
    # frame = cv2.resize(frame,(920,720))

    # 프레임을 RGB로 변환
    image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    # Mediapipe Hand Landmark 모델을 사용하여 이미지 처리
    results = hands.process(image)

    if results.multi_hand_landmarks:
        if len(results.multi_hand_landmarks) == 1:  # 손이 한손만 있을 때
            handLms = results.multi_hand_landmarks[0]
            
        # 각 손가락 끝의 랜드마크 좌표 추출
            fingertips = []
            for finger_tip_id in [4, 8, 12, 16, 20]:
                lm = handLms.landmark[finger_tip_id]
                h, w, c = result.shape   #좌표가 0~1값임.화면상의 픽셀 좌표로 변환하기 위해 이미지의 크기필요 C는 채널
                cx, cy = int(lm.x *w), int(lm.y*h)
                fingertips.append((cx,cy))
            #print('fingertips = ',fingertips)
            # 손가락 끝에 원 그리기
            for location in  fingertips:              
                cv2.circle(result, location, 5, (255, 0, 0), -1)  
                #print('location = ',location)           
                for i in range(len(areas)):                   
                    if is_object_in_area(location, areas[i]):
                        num = str(i)
                        cv2.putText(result, num, (100+i*50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        event = i
                        arr_event.append(event)
                        #print(event)
                        cnt =+ 1
            print ( arr_event)
            if cnt == 0 :
                arr_event = [-1]
            else :
                cnt = 0

            
            if event == prev_event:
                flag = True
                
            elif arr_event != [-1] and not flag and event != prev_event:                   

                pass
            arr_event = []
            arr_prev_event = arr_event  
        else :      
            print("2 hands")
           

           
    # 영역 표시 
    cv2.rectangle(result, (80, 300),(180, 360),(0,0,255),2),  #도 
    cv2.rectangle(result,(180, 300),(280, 360),(54,148,255),2)  #레
    cv2.rectangle(result,(280, 300),(380, 360),(0,228,255),2)  #미
    cv2.rectangle(result,(380, 300),(480, 360),(22,219,29),2)  #파
    cv2.rectangle(result,(480, 300),(580, 360),(22,2,29),2)  #파


    # 결과 보여주기
    cv2.imshow("Fingertip Detection division", result)

    # 'q' 키를 누르면 루프 탈출
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


pygame.midi.quit()
cap.release()
cv2.destroyAllWindows()

