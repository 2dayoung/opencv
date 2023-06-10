import cv2
import mediapipe as mp
import simpleaudio as sa
import pygame.midi
import time
import mido
import numpy as np
import simpleaudio as sa
from tkinter import *

# Initialize Pygame and the MIDI module
pygame.init()
pygame.midi.init()

# Open the MIDI output port
#=========================
'''outport = mido.open_output()
def play_mido(file)  : #outport = mido.open_output()이랑 세트
    mid= mido.MidiFile(file)
    for message in mid.play():
        outport.send(message)
def sound(event,midi_filename):
        music_filename = midi_filename[event]
        play_mido(music_filename)

print("play_mido ")
play_mido("sample135.mid")'''
        

#=========================

#midi filename생성 
midi_filename = []
notes_make_file = [60, 62, 64, 65, 67, 69, 71]
for i, note in enumerate(notes_make_file):    
    midi_filename.append(str(note) +'.mid')
print (midi_filename)

output = pygame.midi.Output(0)
# Define a dictionary that maps note names to MIDI note numbers

def play_note(note_number):
    # Create a note on message and send it to the output port
    note_on = [0x90, note_number, 127]
    output.write_short(*note_on)
    # Wait for a short time to simulate the duration of the note
    time.sleep(1)
    # Create a note off message and send it to the output port
    note_off = [0x80, note_number, 0]
    output.write_short(*note_off)
print("play_note")
play_note(60) #output = pygame.midi.Output(0) 이랑 세트 


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


# 10개의 객체의 위치를 나타내는 리스트
object_locations = [(2, 4), (5, 3), (1, 2), (4, 1), (3, 5), (5, 2), (2, 3), (1, 5), (3, 1), (4, 4)]

# 5개의 영역을 나타내는 리스트, 각각의 영역은 (시작 x 좌표, 시작 y 좌표, 가로 길이, 세로 길이) 형태로 저장
#areas = [(80, 300, 100, 60), (180, 300, 100, 60),(280, 300, 100, 60),(380, 300, 100, 60),(480, 300, 100, 60)]
#영역은 [x,y,w,h] 여야함.
areas = [[53, 384, 53, 48], [106, 384, 53, 48], [159, 384, 53, 48],
 [212, 384, 53, 48], [265, 384, 53, 48], [318, 384, 53, 48],
 [371, 384, 53, 48], [424, 384, 53, 48], [477, 384, 53, 48],
 [530, 384, 53, 48]]

prev_event = None
arr_prev_event = None
prev_event2 = None
arr_prev_event2 = None
prev_event1 = None
arr_prev_event1 = None
music_playing = False
flag = False
event = 0
arr_event = []
arr_event1 = []
arr_event2 = []
cnt = 0
while True:
    # 웹캠에서 프레임 읽기& 좌우반전 &크기
    ret, frame = cap.read()
    
    #frame = cv2.resize(frame,(920,720))
    result= cv2.flip(frame,1) 
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

            # 손가락 끝에 원 그리기
            outflag = False  
            for location in  fingertips:              
                cv2.circle(result, location, 5, (255, 0, 0), -1)  
                #print('location = ',location)
                            
                for i in range(len(areas)):                   
                    if is_object_in_area(location, areas[i]):
                        event = i
                        arr_event.append(event)
                        cnt =+ 1

            #중복요소 제거
            arr_event=set(arr_event)
            arr_event=list(arr_event)
            if arr_prev_event != arr_event:
                if arr_event != [] :
                    event =arr_event[0]
                    play_note(60+event)  
                    
                print (arr_event)
                pass

            arr_prev_event = arr_event 
            arr_event = [] 

        # 양손다 들어왔을때    
        else :      
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


            outflag1 = False  
            for location in  fingertips1:
                #왼손 손가락 끝 점으로 표시              
                cv2.circle(result, location, 5, (255, 0, 0), -1)  
                #영역안에 들어왔을 경우 array에 추가 
                for i in range(len(areas)):                   
                    if is_object_in_area(location, areas[i]):
                        event = i
                        arr_event1.append(event)
                        
                        cnt =+ 1 
            #중복요소 제거
            arr_event1=set(arr_event1)
            #리스트로 변경
            arr_event1=list(arr_event1)
            if arr_prev_event1 != arr_event1:
                if arr_event1 != [] :
                    event =arr_event1[0]
                    play_note(60+event)  
                print ("Arr 1 ", arr_event1)        
                pass
            #print ( arr_event)
            arr_prev_event1 = arr_event1 
            arr_event1 = [] 
            #print ( "prev",arr_prev_event)

            #오른손
            outflag2 = False  
            for location in  fingertips2:              
                cv2.circle(result, location, 5, (255, 0, 0), -1)  

                for i in range(len(areas)):                   
                    if is_object_in_area(location, areas[i]):
                        event = i
                        arr_event2.append(event)
                        
                        cnt =+ 1

            #중복요소 제거
            arr_event2=set(arr_event2)
            #리스트로 변경
            arr_event2=list(arr_event2)
            if arr_prev_event2 != arr_event2:
                if arr_event2 != [] :
                    event =arr_event2[0]
                    play_note(60+event)  
                print ("Arr 2 ", arr_event2)        
                pass

            #print ( arr_event)
            arr_prev_event2 = arr_event2
            arr_event2 = [] 
            #print ( "prev",arr_prev_event)

    #영역에 사각형으로 표시 
    for area in areas:
        cv2.rectangle(result, (area[0], area[1]),(area[0]+area[2],area[1]+area[3]), (0, 255, 0), 2)



    # 결과 보여주기
    cv2.imshow("Fingertip Detection division", result)

    # 'q' 키를 누르면 루프 탈출
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 해제 및 모든 윈도우 종료
output.close()
pygame.midi.quit()
cap.release()
cv2.destroyAllWindows()
    