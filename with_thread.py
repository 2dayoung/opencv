import threading
import pygame
from threading import Thread, Lock
import mido
import cv2
import mediapipe as mp


#======================================================================
#함수
#======================================================================

# midi filename 생성
midi_filename = []
notes_make_file = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76]
for i, note in enumerate(notes_make_file):    
    midi_filename.append(str(note) + '.mid')
print(midi_filename)

# play_mido 함수
outport = mido.open_output()
def play_mido(midi_filename):
    mid = mido.MidiFile(midi_filename)
    for message in mid.play():
        outport.send(message)

def is_object_in_area(object_location, area):
    x, y = object_location
    start_x, start_y, width, height = area
    return start_x <= x < start_x + width and start_y <= y < start_y + height

#=====================================================================
# Mediapipe Hand Landmark 모델 초기화
#=====================================================================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, 
                    max_num_hands=2, 
                    min_detection_confidence=0.7, 
                    min_tracking_confidence=0.7)



#=====================================================================
# mediapipe 변수 선언
#=====================================================================
# 10개의 객체의 위치를 나타내는 리스트
object_locations = [(2, 4), (5, 3), (1, 2), (4, 1), (3, 5), (5, 2), (2, 3), (1, 5), (3, 1), (4, 4)]

#영역은 [x,y,w,h] 여야함.
areas = [[53, 384, 53, 48], [106, 384, 53, 48], [159, 384, 53, 48],
 [212, 384, 53, 48], [265, 384, 53, 48], [318, 384, 53, 48],
 [371, 384, 53, 48], [424, 384, 53, 48], [477, 384, 53, 48],
 [530, 384, 53, 48]]





arr1_event = []
#=====================================================================
# 종료 신호를 전달하기 위한 이벤트 객체
exit_event = threading.Event()
#=====================================================================



def cam():
    # global 변수  
    global arr1_event

    cap = cv2.VideoCapture(0)
    cnt = 0
    arr_event = []
    arr_event1 = []
    arr_event2 = []
    arr_prev_event = None
    prev_event2 = None
    arr_prev_event2 = None
    prev_event1 = None
    arr_prev_event1 = None


    while not exit_event.is_set():
        # 웹캠에서 프레임 읽기& 좌우반전 &크기
        ret, frame = cap.read()
        result = cv2.flip(frame, 1)
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

                              
                for location in  fingertips:
                    # 손가락 끝에 원 그리기              
                    cv2.circle(result, location, 5, (255, 0, 0), -1)  
                    #영역에 들어왔는지 검사            
                    for i in range(len(areas)):                   
                        if is_object_in_area(location, areas[i]):
                            event = i
                            arr_event.append(event)
                            
                #중복요소 제거
                arr_event=set(arr_event)
                arr_event=list(arr_event)

                #전 array와 다르면 global변수로 전달 
                if arr_prev_event != arr_event:
                    arr1_event = arr_event                                       
                    print (arr_event)
                    pass

                arr_prev_event = arr_event 
                arr_event = [] 

            # 양손다 들어왔을때    
            else :      
                pass
                handLms1 = results.multi_hand_landmarks[0]  # 왼손
                handLms2 = results.multi_hand_landmarks[1]  # 오른손

            # 각 손가락 끝의 랜드마크 좌표 추출 (왼손)
                fingertips1 = []
                for finger_tip_id in [4, 8, 12, 16, 20]:
                    lm = handLms1.landmark[finger_tip_id]
                    h, w, c = result.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    fingertips1.append((cx, cy))
                
            # 각 손가락 끝의 랜드마크 좌표 추출 (오른손)
                fingertips2 = []
                for finger_tip_id in [4, 8, 12, 16, 20]:
                    lm = handLms2.landmark[finger_tip_id]
                    h, w, c = result.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    fingertips2.append((cx, cy))
                #왼손
                for location in  fingertips1:       
                    cv2.circle(result, location, 5, (255, 0, 0), -1)  
                    #영역안에 들어왔을 경우 array에 추가 
                    for i in range(len(areas)):                   
                        if is_object_in_area(location, areas[i]):
                            event = i
                            arr_event1.append(event)
                #오른손
                for location in  fingertips2:              
                    cv2.circle(result, location, 5, (255, 0, 0), -1)  
                    #영역안에 들어왔을 경우 array에 추가
                    for i in range(len(areas)):                   
                        if is_object_in_area(location, areas[i]):
                            event = i
                            arr_event1.append(event)            
                            

                #중복요소 제거
                arr_event1=set(arr_event1)
                #리스트로 변경
                arr_event1=list(arr_event1)

                if arr_prev_event1 != arr_event1:                        
                    arr1_event = arr_event1                                       
                    print ("양손",arr_event1)
                    pass

                arr_prev_event1 = arr_event1 
                arr_event1 = [] 

        #영역에 사각형으로 표시 
        for area in areas:
            cv2.rectangle(result, (area[0], area[1]),(area[0]+area[2],area[1]+area[3]), (0, 255, 0), 2)

        cv2.imshow("Fingertip Detection division", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit_event.set()  # 종료 신호 설정
            break
        
    cap.release()
    cv2.destroyAllWindows()

# Thread list 생성
threads_list = []

# 카메라 스레드 추가
cam_thread = threading.Thread(target=cam)
cam_thread.start()
prev_arr1 = []

while not exit_event.is_set():
    while arr1_event != [] and arr1_event != prev_arr1 :
        print(arr1_event)
        prev_arr1 = arr1_event 
        threads_list = []
        # MIDI 파일 재생 스레드 추가
        for i in arr1_event:
            midi_thread = threading.Thread(target=play_mido, args=(midi_filename[i],))
            threads_list.append(midi_thread)

        for t in threads_list:
            t.start()

        for t in threads_list:
            t.join()
    

cam_thread.join()
print('End')

# 종료
pygame.mixer.quit()
pygame.quit()
