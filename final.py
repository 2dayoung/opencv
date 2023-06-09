import cv2
import mediapipe as mp
import simpleaudio as sa
import pygame.midi
import mido
import numpy as np
from tkinter import *
import threading
import pygame
from threading import Thread, Lock


#=====================================================================
# 필요한 함수 정의 
#=====================================================================

midi_filename = []
notes_make_file = [48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71]
for i, note in enumerate(notes_make_file):
    midi_filename.append(str(note) + '.mid')

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

mouse_drag_started = False
mouse_click_count =0
roi_points=[]

def mouse_callback(event, x, y, flags, param):
    global mouse_drag_started, roi_points, mouse_click_count

    if event == cv2.EVENT_LBUTTONDOWN:
        if mouse_click_count < 10:
                # 좌표 출력
            print(f"Clicked: ({x}, {y})")
            roi_points.append((x, y))
            mouse_click_count += 1
            
        if mouse_click_count == 2:
            mouse_click_count=0           
            divide_area()
            mouse_drag_started=True
            roi_points=[]

#영역은 [x,y,w,h] 여야함             
areas = []
black=[0, 1, 3, 4, 5, 7, 8, 10, 11, 12]

def divide_area(): #건반영역 좌표 설정 
    global areas,roi_points
    x1 = roi_points[0][0]
    x2 = roi_points[1][0]
    y1 = roi_points[0][1]
    n=14
    width = x2 - x1
    area_width = width // n
    for i in range(n):
        area_x = x1 + (i * area_width)
        area_y = y1
        area_w = area_width
        area_h = 50
        if i == n - 1:
            area_w = width - (i * area_width)
        areas.append([area_x, area_y, area_w, area_h])

def which_note():
    # global 변수  
    global pressed_keys, mouse_drag_started,black

     # Mediapipe Hand Landmark 모델 초기화
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, 
                        max_num_hands=2, 
                        min_detection_confidence=0.7, 
                        min_tracking_confidence=0.7)

    cap = cv2.VideoCapture(0)

    cv2.namedWindow("piano")
    cv2.setMouseCallback("piano", mouse_callback)

    onehand_event = []
    twohands_event = []

    while not exit_event.is_set() :
        
        # 웹캠에서 프레임 읽기& 좌우반전 &크기
        ret, frame = cap.read()
        result = cv2.flip(frame, 1)
        cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 현재 캠의 가로 해상도
        cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 현재 캠의 세로 해상도           
        width = cap_width * 1.5
        height = cap_height * 1.5           
        result = cv2.resize(result, (int(width), int(height)), interpolation=cv2.INTER_LINEAR)
        
        cv2.imshow("piano", result)
        if mouse_drag_started:
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
                    # 영역에 들어왔는지 검사하고 list에 추가             
                        for i in range(len(areas)):                   
                            if is_object_in_area(location, areas[i]):
                                event = i
                                onehand_event.append(event)
                                
                #중복요소 제거
                    onehand_event=set(onehand_event)
                    pressed_keys=list(onehand_event)

                #리스트 초기화
                    onehand_event = [] 

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

                # 왼손영역안에 들어왔을 경우 list에 추가 
                    for location in  fingertips1:       
                        cv2.circle(result, location, 5, (255, 0, 0), -1)  
                        for i in range(len(areas)):                   
                            if is_object_in_area(location, areas[i]):
                                event = i
                                twohands_event.append(event)

                # 오른손영역안에 들어왔을 경우 list에 추가
                    for location in  fingertips2:              
                        cv2.circle(result, location, 5, (255, 0, 0), -1)  
                        for i in range(len(areas)):                   
                            if is_object_in_area(location, areas[i]):
                                event = i
                                twohands_event.append(event)            
                                
                # 중복요소 제거
                    twohands_event=set(twohands_event)
                # 리스트로 변경
                    pressed_keys=list(twohands_event)
                # 리스트 초기화
                    twohands_event = [] 
            
            # 영역 사각형으로 표시 
            for i, area in enumerate(areas):
                cv2.rectangle(result, (area[0], area[1]),(area[0]+area[2],area[1]+area[3]),(0,0,0), 2)
                if i in black :
                    cv2.circle(result, (area[0]+area[2], area[1]+7), int(area[2]*0.3), (0,0,0), -1)
                if i ==7 :
                    cv2.putText(result,"C4", (area[0] + 5,area[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
            # 눌린 건반 색으로 표시 
            for idx in pressed_keys:
                area = areas[idx]
                cv2.rectangle(result, (area[0], area[1]), (area[0] + area[2], area[1] + area[3]), (200, 200, 25), thickness=cv2.FILLED)

        cv2.imshow("piano", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit_event.set()  # 종료 신호 설정
            break

    cap.release()
    cv2.destroyAllWindows()

#=====================================================================
# piano선택시 실행 함수 
#=====================================================================
def compare_lists(list1, list2):
    changed_elements = set(list2) - set(list1)  # 두 집합의 차집합을 구함
    return list(changed_elements)  # 결과를 리스트로 변환하여 반환

def piano():
    # 종료 신호를 전달하기 위한 이벤트 객체
    global exit_event
    exit_event = threading.Event()

    global pressed_keys
    pressed_keys = []

    # 카메라 스레드 추가
    cam_thread = threading.Thread(target=which_note)
    cam_thread.start()
    previous_key = []

    while not exit_event.is_set():
        while pressed_keys != [] and pressed_keys != previous_key :
            
            threads_list = []

            # 리스트로 변경
            pressed_key=compare_lists(pressed_keys, previous_key)
            print(pressed_key)
            # MIDI 파일 재생 스레드 생성, 추가
            for i in pressed_key:
                midi_thread = threading.Thread(target=play_mido, args=(midi_filename[i],))
                threads_list.append(midi_thread)
                
            #스레드 실행
            for t in threads_list:
                t.start()

            # #스레드 끝날때 까지 대기 
            # for t in threads_list:
            #     t.join()

            previous_key = pressed_keys 

    cam_thread.join()
    print('End')

    # 종료
    pygame.mixer.quit()
    pygame.quit()
        
#=====================================================================
# drum선택시 실행 함수 
#=====================================================================
def drum() : 
    global mouse_click_count_drum, roi_points_drum, mouse_drag_started_drum, rectangles_drum
    mouse_click_count_drum = 0
    roi_points_drum = []
    mouse_drag_started_drum = False
    rectangles_drum = []

    def mouse_callback(event, x, y, flags, param):
        global mouse_drag_started_drum, roi_points_drum, mouse_click_count_drum, rectangles_drum

        if event == cv2.EVENT_LBUTTONDOWN:
            if mouse_click_count_drum < 2:
                # 좌표 출력
                print(f"Clicked: ({x}, {y})")
                roi_points_drum.append((x, y))
                mouse_click_count_drum += 1

            if mouse_click_count_drum == 2:
                mouse_click_count_drum = 0
                mouse_drag_started_drum = True
                roi_points_drum = roi_points_drum[-2:]  

                if len(rectangles_drum) < 4:
                    x1, y1 = roi_points_drum[0]
                    x2, y2 = roi_points_drum[1]
                    rectangles_drum.append((x1, y1, x2, y2))

                else:
                    mouse_drag_started_drum = False

    cap = cv2.VideoCapture(0)
    cv2.namedWindow('drum')

    # 드럼 소리를 재생할 오디오 파일 경로
    drum_sound1 = sa.WaveObject.from_wave_file('drum/hihat.wav')
    drum_sound2 = sa.WaveObject.from_wave_file('drum/snare.wav')
    drum_sound3 = sa.WaveObject.from_wave_file('drum/mid_tom.wav')
    drum_sound4 = sa.WaveObject.from_wave_file('drum/kick.wav')

    event = None
    prev_event = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if not ret:
            break

        # 가로 해상도를 조정
        cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 현재 캠의 가로 해상도
        cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 현재 캠의 세로 해상도           
        width = cap_width * 1.5
        height = cap_height * 1.5           
        result_drum = cv2.resize(frame, (int(width), int(height)), interpolation=cv2.INTER_LINEAR)
        
        # 이미지를 BGR에서 HSV로 변환
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.setMouseCallback('drum', mouse_callback)

        # 앞서 그린 사각형들이 안 없어지도록 
        for i, rect in enumerate(rectangles_drum):
            x1, y1, x2, y2 = rect
            color = [(0, 165, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)][i]
            cv2.rectangle(result_drum, (x1, y1), (x2, y2), color, 2)

        cv2.imshow('drum', result_drum)

        # 객체 색범위 
        lower_blue = (90, 100, 100)
        upper_blue = (120, 255, 255)

        # 마스크 생성
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        kernel = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        #cv2.imshow("closing ",closing )
        
        # 객체 검출
        contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 두 개의 가장 큰 객체만 추출
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

        # 모든 영역 클릭하면 실행
        if contours and len(rectangles_drum) > 3:
            # 두 개의 객체에 대한 event 초기화
            event = [-1, -1] 
            for i, c in enumerate(contours):
                x, y, w, h = cv2.boundingRect(c)
                cx = x + w // 2
                cy = y + h // 2
        
            # 중심 좌표를 사용하여 소리 재생
                if rectangles_drum[0][0] < cx < rectangles_drum[0][2] and rectangles_drum[0][1] < cy < rectangles_drum[0][3]:
                    event[i] = 1
                elif rectangles_drum[1][0] < cx < rectangles_drum[1][2] and rectangles_drum[1][1] < cy < rectangles_drum[1][3]:
                    event[i] = 2
                elif rectangles_drum[2][0] < cx < rectangles_drum[2][2] and rectangles_drum[2][1] < cy < rectangles_drum[2][3]:
                    event[i] = 3
                elif rectangles_drum[3][0] < cx < rectangles_drum[3][2] and rectangles_drum[3][1] < cy < rectangles_drum[3][3]:
                    event[i] = 4
            # 객체 표시
                cv2.circle(result_drum,(cx,cy),max(w,h)//2,(255,255,255),2)

            # 두 개의 event 값을 독립적으로 처리
            if event[0] != -1:
                if event[0] == prev_event[0]:
                    pass
                elif event[0] == 1:
                    drum_sound1.play()
                    print("play", event[0])
                elif event[0] == 2:
                    drum_sound2.play()
                    print("play", event[0])
                elif event[0] == 3:
                    drum_sound3.play()
                    print("play", event[0])
                elif event[0] == 4:
                    drum_sound4.play()
                    print("play", event[0])

            if event[1] != -1:
                if event[1] == prev_event[1]:
                    pass
                elif event[1] == 1:
                    drum_sound1.play()
                    print("play", event[1])
                elif event[1] == 2:
                    drum_sound2.play()
                    print("play", event[1])
                elif event[1] == 3:
                    drum_sound3.play()
                    print("play", event[1])
                elif event[1] == 4:
                    drum_sound4.play()
                    print("play", event[1])

            prev_event = event
            print(event)
        
        # 결과 출력
        cv2.imshow('drum', result_drum)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def start():
    root = Tk()
    root.title("Motion Play")

    # 윈도우 크기 설정
    window_width = 720
    window_height = 480
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    # 라벨 추가
    label = Label(root, text="연주할 악기를 선택하세요", font=("함초롬돋음", 18))
    label.configure(font=("휴먼엑스포", 20))
    label.place(relx=0.5, rely=0.55, anchor="center")
    title = Label(root, text="Motion Play")
    title.configure(font=("Perpetua Titling MT", 50))
    title.place(relx=0.5, rely=0.3, anchor="center")

    # 버튼 추가
    piano_button = Button(root, text="피아노",command= piano)
    piano_button.configure(font=("휴먼엑스포", 20))
    piano_button.place(relx=0.3, rely=0.7, anchor="center")
    piano_button.config(width=8, height=2)

    drum_button = Button(root, text="드럼",command= drum)
    drum_button.configure(font=("휴먼엑스포", 20))
    drum_button.place(relx=0.7, rely=0.7, anchor="center")
    drum_button.config(width=8, height=2)
    drum_button.config()

    root.mainloop()

if __name__ == '__main__':
    start()
