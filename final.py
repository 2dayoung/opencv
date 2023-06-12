import cv2
import mediapipe as mp
import simpleaudio as sa
import pygame.midi
import time
import mido
import numpy as np
from tkinter import *
import threading
import pygame
from threading import Thread, Lock
from PIL import Image, ImageFont, ImageDraw

def piano():
    midi_filename = []
    notes_make_file = [48, 50, 52, 53, 55, 57, 59,60, 62, 64, 65, 67, 69, 71]
    for i, note in enumerate(notes_make_file):    
        midi_filename.append(str(note) + '.mid')
    print(midi_filename)

    # play_mido 함수
    outport = mido.open_output()
    def play_mido(midi_filename):
        mid = mido.MidiFile(midi_filename)
        for message in mid.play():
            outport.send(message)
        print(midi_filename)

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
    # areas = [[53, 384, 53, 48], [106, 384, 53, 48], [159, 384, 53, 48],
    # [212, 384, 53, 48], [265, 384, 53, 48], [318, 384, 53, 48],
    # [371, 384, 53, 48], [424, 384, 53, 48], [477, 384, 53, 48],
    # [530, 384, 53, 48]]

    global mouse_click_count 
    global roi_points 
    global mouse_drag_started
    mouse_drag_started = False
    mouse_click_count =0
    roi_points=[]
    def mouse_callback(event, x, y, flags, param):
        global mouse_drag_started,roi_x, roi_y, roi_width, roi_height, roi_points, mouse_click_count

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
                print("true")
                roi_points=[]
    global areas
    areas = []
    global black
    black=[0, 1, 3, 4, 5, 7, 8, 10, 11, 12]
    def divide_area():
        global areas,roi_points
        x1 =roi_points[0][0]
        x2 = roi_points[1][0]
        y1= roi_points[0][1]
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
            
        print(areas)  
    
    global arr1_event
    arr1_event = []
    #=====================================================================
    # 종료 신호를 전달하기 위한 이벤트 객체
    exit_event = threading.Event()
    #=====================================================================
    # 마우스 이벤트 콜백 등록


    #=====================================================================

    def cam():
        # global 변수  
        global arr1_event, mouse_drag_started,black

        
        cap = cv2.VideoCapture(0)

        cv2.namedWindow("paino")
        cv2.setMouseCallback("paino", mouse_callback)

        cnt = 0
        arr_event = []
        arr_event1 = []
        arr_event2 = []
        arr_prev_event = None
        prev_event2 = None
        arr_prev_event2 = None
        prev_event1 = None
        arr_prev_event1 = None


        while not exit_event.is_set() :
            
            # 웹캠에서 프레임 읽기& 좌우반전 &크기
            ret, frame = cap.read()
            result = cv2.flip(frame, 1)

            # 가로 해상도를 조정
            cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 현재 캠의 가로 해상도
            cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 현재 캠의 세로 해상도           
            width = cap_width * 1.5
            height = cap_height * 1.5           
            result = cv2.resize(result, (int(width), int(height)), interpolation=cv2.INTER_LINEAR)
            
            cv2.imshow("paino", result)
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
                            #print (arr_event)
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
                            #print ("양손",arr_event1)
                            pass

                        arr_prev_event1 = arr_event1 
                        arr_event1 = [] 
                
                #영역에 사각형으로 표시 
                for i, area in enumerate(areas):
                    cv2.rectangle(result, (area[0], area[1]),(area[0]+area[2],area[1]+area[3]),(0,0,0), 2)
                    if i in black :
                        cv2.circle(result, (area[0]+area[2], area[1]+7), int(area[2]*0.3), (0,0,0), -1)
                    if i ==7 :
                        cv2.putText(result,"C4",(area[0]+5,area[1]+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
                for idx in arr1_event:
                    area = areas[idx]
                    cv2.rectangle(result, (area[0], area[1]), (area[0] + area[2], area[1] + area[3]), (200, 200, 25), thickness=cv2.FILLED)
            cv2.imshow("paino", result)

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
            #print(arr1_event)
            
            threads_list = []
            #different_notes = [num for num in arr1_event if num not in prev_arr1]
            #print("diff",different_notes)
            # MIDI 파일 재생 스레드 추가
            for i in arr1_event:
                midi_thread = threading.Thread(target=play_mido, args=(midi_filename[i],))
                threads_list.append(midi_thread)

            for t in threads_list:
                t.start()

            for t in threads_list:
                t.join()
            prev_arr1 = arr1_event 

    cam_thread.join()
    print('End')

    # 종료
    pygame.mixer.quit()
    pygame.quit()
        

def drum() : 
    global mouse_click_count_drum,roi_points_drum,mouse_drag_started_drum,rectangles_drum
    mouse_click_count_drum = 0
    roi_points_drum = []
    mouse_drag_started_drum = False
    rectangles_drum = []

    def play_drum_sound(sound_file):
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()

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
        frame = cv2.resize(frame, (int(width), int(height)), interpolation=cv2.INTER_LINEAR)
        
        # 이미지를 BGR에서 HSV로 변환
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        img = frame.copy()
        cv2.setMouseCallback('drum', mouse_callback)

        if mouse_drag_started_drum:
            x1, y1 = roi_points_drum[0]
            x2, y2 = roi_points_drum[1]

            color = [(255, 165, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)][len(rectangles_drum)]

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # 앞서 그린 사각형들이 안 없어지도록 
        for i, rect in enumerate(rectangles_drum):
            x1, y1, x2, y2 = rect
            color = [(0, 165, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)][i]
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        cv2.imshow('drum', img)

        lower_blue = (90, 100, 100)
        upper_blue = (120, 255, 255)


        # HSV 이미지에서 색상 범위에 해당하는 영역을 이진화합니다.
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # 잡음 제거를 위한 모폴로지 연산
        kernel = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow("closing ",closing )
        
        # 객체 검출
        contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 두 개의 가장 큰 객체만 추출
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

        if contours and len(rectangles_drum) > 3:
            # 객체 위치 추출
            event = [-1, -1]  # 두 개의 객체에 대한 event 초기화
            for i, c in enumerate(contours):
                x, y, w, h = cv2.boundingRect(c)
                cx = x + w // 2
                cy = y + h // 2
        
                # 원 중심 좌표를 사용하여 소리 재생
                if rectangles_drum[0][0] < cx < rectangles_drum[0][2] and rectangles_drum[0][1] < cy < rectangles_drum[0][3]:
                    event[i] = 1
                elif rectangles_drum[1][0] < cx < rectangles_drum[1][2] and rectangles_drum[1][1] < cy < rectangles_drum[1][3]:
                    event[i] = 2
                elif rectangles_drum[2][0] < cx < rectangles_drum[2][2] and rectangles_drum[2][1] < cy < rectangles_drum[2][3]:
                    event[i] = 3
                elif rectangles_drum[3][0] < cx < rectangles_drum[3][2] and rectangles_drum[3][1] < cy < rectangles_drum[3][3]:
                    event[i] = 4
                    

                # cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), (255,255,255), 2)
                cv2.circle(img,(cx,cy),max(w,h)//2,(255,255,255),2)
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
        cv2.imshow('drum', img)

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
