import cv2
import mediapipe as mp
import simpleaudio as sa
import pygame.midi
import time
import numpy as np
import simpleaudio as sa

print("연주할 악기를 선택하세요")
print("1. 피아노 \n2.드럼\n3. 나가기")

while True:
    menu = input("연주할 악기를 선택해주세요 : ")

    if menu=='1':

        # Initialize Pygame and the MIDI module
        pygame.init()
        pygame.midi.init()

        # Get the ID of the first output device
        device_id = pygame.midi.get_default_output_id()

        # Open the MIDI output port
        output = pygame.midi.Output(device_id)

        # Define a dictionary that maps note names to MIDI note numbers
        notes = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}

        def play_note(note_name):
            # Convert the note name to a MIDI note number
            note_number = notes[note_name]
            # Create a note on message and send it to the output port
            note_on = [0x90, note_number, 127]
            output.write_short(*note_on)
            # Wait for a short time to simulate the duration of the note
            time.sleep(0.5)
            # Create a note off message and send it to the output port
            note_off = [0x80, note_number, 0]
            output.write_short(*note_off)

        def is_object_in_area(object_location, area):
            x, y = object_location
            start_x, start_y, width, height = area
            return start_x <= x < start_x + width and start_y <= y < start_y + height

        def play_note_by_position(position):
            #판별된 건반의 위치에 따라 해당되는 소리 재생
            if position == 1:
                play_note('C')
            elif position == 2:
                play_note('D')
            elif position == 3:
                play_note('E')
            elif position == 4:
                play_note('F')
            elif position == 5:
                play_note('G')


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

        def check_finger_in_area(finger_location, areas):
            for i in range(len(areas)):
                if is_object_in_area(finger_location, areas[i]):
                    return i+1
                return None

        while True:
            # 영상 취득
            ret, frame = cap.read()
            result=cv2.flip(frame,1)
            
            # 흑백 영상으로 변환
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 프레임을 RGB로 변환
            image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

            # Mediapipe Hand Landmark 모델을 사용하여 이미지 처리
            results = hands.process(image)

            # 이진화
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

            # 노이즈 제거
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

            # 윤곽선 검출
            contours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)            

            #def assign_key_position(key_area, position):
              #  white_key_position = position // 2+1    #흰색 건반의 위치
                #if position % 2 ==0:    #짝수인 경우 (검은색 건반)
                  #  black_key_position = white_key_position - 1     #흰색 건반의 왼쪽에 위치
                    #return black_key_position
                #else:   #홀수인 경우 (흰색 건반)
                  #  return white_key_position

            # 건반 영역 추출 및 넘버링
            key_area = []
            position = 1
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if h > 100 and w > 20:
                    #건반의 높이와 너비를 보정하여 정확한 영역 추출
                    h=int(h * 1.2)
                    w=int(w * 0.8)
                    y -=int (h * 0.1)
                    x +=int ((w-w*0.8)/2)
                    
                    key_area.append([x, y, w, h])
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, str(position), (x+int(w/2), y+int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    position += 1

        # Mediapipe Hand Landmark 모델을 사용하여 이미지 처리
            results = hands.process(image)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    # 각 손가락 끝의 랜드마크 좌표 추출
                    fingertips = []
                    for finger_tip_id in [4, 8, 12, 16, 20]:
                        lm = handLms.landmark[finger_tip_id]
                        h, w, c = result.shape   #좌표가 0~1값임.화면상의 픽셀 좌표로 변환하기 위해 이미지의 크기필요 C는 채널
                        cx, cy = int(lm.x *w), int(lm.y*h)
                        fingertips.append((cx,cy))

                    # 손가락 끝에 원 그리기
                    for fingertip in  fingertips:              
                        cv2.circle(result, fingertip, 5, (255, 0, 0), -1)
                        # print("(x,y) =",fingertip[1])  
                        # print("(x,y) =",fingertip)               
                        cnt +=1
                        object_locations = fingertips

                    #5개씩 구분
                    if cnt == 5 :
                        # print(fingertips)
                        # print("===========")               
                        cnt=0
            
                    # 모든 객체가 영역 내에 있는지 검사
                    for i in range(len(key_area)):
                        for location in object_locations:
                            if is_object_in_area(location, key_area[i]):
                                num = str(i)
                                cv2.putText(result, num, (100+i*50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                                if position == 1:
                                    play_note('C')
                                elif position == 2:
                                    play_note('D')
                                elif position == 3:
                                    play_note('E')
                                elif position == 4:
                                    play_note('F')
                                elif position ==5:
                                    play_note('G')
                                elif position ==6:
                                    play_note('A')
                                elif position == 7:
                                    play_note('B')
                                elif position == 8:
                                    play_note('C')
                                elif position ==9:
                                    play_note('D')

            # 화면에 출력
            cv2.imshow('frame', frame)


            # 종료 조건
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 웹캠 해제 및 모든 윈도우 종료
        cap.release()
        cv2.destroyAllWindows()
        output.close()
        pygame.midi.quit()
    

    elif menu == '2':

        def play_drum(sound_file):
            wave_obj = sa.WaveObject.from_wave_file(sound_file)
            play_obj = wave_obj.play()
            play_obj.wait_done()

        # 웹캠 초기화
        cap = cv2.VideoCapture(0)

        # 드럼 소리를 재생할 오디오 파일 경로
        drum_sound1 = 'kick.wav'
        drum_sound2 = 'snare.wav'
        drum_sound3 = 'hihat.wav'

        # 직사각형 영역 정보
        rectangle1 = [(80, 250), (180, 400)]  # 좌상단, 우하단 좌표
        rectangle2 = [(280, 250), (380, 400)]
        rectangle3 = [(480, 250), (580, 400)]

        while True:
            # 웹캠에서 프레임 읽기
            ret, frame = cap.read()

            # 프레임을 RGB로 변환
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            #원 감지
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=100, param1=50, param2=30, minRadius=10, maxRadius=100)

            # 직사각형 그리기
            cv2.rectangle(frame, rectangle1[0], rectangle1[1], (0, 0, 255), 2)
            cv2.rectangle(frame, rectangle2[0], rectangle2[1], (0, 255, 0), 2)
            cv2.rectangle(frame, rectangle3[0], rectangle3[1], (255, 0, 0), 2)

            #원이 감지되면 소리 재생
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for circle in circles[0]:
                    cx, cy = circle[0], circle[1]

                    #원 중심 좌표를 사용하여 소리 재생
                    if 80< cx < 180 and 250< cy <400:
                        play_drum(drum_sound1)
                    elif 280< cx < 380 and 250 < cy <400:
                        play_drum(drum_sound2)
                    elif 480 < cx < 580 and 250 < cy < 400:
                        play_drum(drum_sound3)

                    #원 그리기
                    cv2.circle(frame, (cx, cy), circle[2], (0, 255, 0), 2)

            #결과 출력
            cv2.imshow('Drume Detection', frame)

            #'q' 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        #웹캠 해제 및 창 닫기
        cap.release()
        cv2.destroyAllWindows()


    if menu=='3':
        break
        
    else:
        print("메뉴를 다시 선택해 주세요.")
        continue
