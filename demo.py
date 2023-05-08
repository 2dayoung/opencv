import cv2
import mediapipe as mp
import simpleaudio as sa
import pygame.midi
import time
import mido

#=========================
#원래 있던 midi 파일 실행   play_music()
#=========================

import pygame

#midi filename생성 
midi_filename = []
notes = [60, 62, 64, 65, 67, 69, 71]
for i, note in enumerate(notes):    
    midi_filename.append(str(note) +'.mid')
    
# mixer config
freq = 44100  # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024   # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)

# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.4)

def play_music(midi_filename):
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.play()
    

print("play_music")
play_music('60.mid')
print("play_music end")


''' 이거 쓰려면 이렇게 (안됨)
    for i in range(len(areas)):
            if is_object_in_area(location, areas[i]):
                num = str(i)
                cv2.putText(result, num, (100+i*50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                event = i
                if event == 0:
                    music_filename = midi_filename[event]
                    break
                elif event == 1:
                    music_filename = midi_filename[event]
                    break
                elif event == 2:
                    music_filename = midi_filename[event]
                    break
                elif event == 3:
                    music_filename = midi_filename[event]
                    break
                elif event == 4:
                    music_filename = midi_filename[event]
                    break

        if music_filename != "" and not music_playing:
            play_music(music_filename)
            print('play', music_filename)
            music_playing = True
        
        if music_playing and not is_object_in_any_area(location, areas):
            stop_music()
            print('stop', music_filename)
            music_playing = False
            music_filename = ""'''
#=====================

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#============================
'''
만들어서 재생  play_note()
'''
# Initialize Pygame and the MIDI module
pygame.init()
pygame.midi.init()

# Get the ID of the first output device
device_id = pygame.midi.get_default_output_id()
print(device_id)

# Open the MIDI output port
output = pygame.midi.Output(device_id)

# Define a dictionary that maps note names to MIDI note numbers
notes = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69}
#=========================
def sound(event,midi_filename):
        music_filename = midi_filename[event]
        play_mido(music_filename)
#       print('play', music_filename)
        print(event)
print (midi_filename)
#=========================

#

def play_note(note_name):
    # Convert the note name to a MIDI note number
    note_number = notes[note_name]
    # Create a note on message and send it to the output port
    note_on = [0x90, note_number, 127]
    output.write_short(*note_on)
    # Wait for a short time to simulate the duration of the note
    time.sleep(1)
    # Create a note off message and send it to the output port
    note_off = [0x80, note_number, 0]
    output.write_short(*note_off)

def is_object_in_area(object_location, area):
    x, y = object_location
    start_x, start_y, width, height = area
    return start_x <= x < start_x + width and start_y <= y < start_y + height
# 밑에 수정 이렇게 
#============================================
'''
            for i in range(len(areas)):
                for location in object_locations:
                    if is_object_in_area(location, areas[i]):
                        num = str(i)
                        cv2.putText(result, num, (100+i*50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        event = i
                        if event == 1:
                            play_note('C')
                        elif event == 2:
                            play_note('D')
                        elif event == 3:
                            play_note('E')
                        elif event == 4:
                            play_note('F')'''
#============================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


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
#areas = [(80, 300, 100, 60), (180, 300, 100, 60),(280, 300, 100, 60),(380, 300, 100, 60),(480, 300, 100, 60)]
areas = [[53, 384, 106, 432], [106, 384, 159, 432],
          [159, 384, 212, 432], [212, 384, 265, 432], 
          [265, 384, 318, 432], [318, 384, 371, 432],
            [371, 384, 424, 432], [424, 384, 477, 432],
              [477, 384, 530, 432], [530, 384, 583, 432]]
def stop_music():
    pygame.mixer.music.stop()

outport = mido.open_output()

def play_mido(file) :
    mid= mido.MidiFile(file)
    for message in mid.play():
        outport.send(message)

prev_event = None
music_playing = False
flag = False
event = 0
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
                object_locations = fingertips

            outflag = False
            for location in object_locations:
                flag = True
                for i in range(len(areas)):
                    
                    if is_object_in_area(location, areas[i]):
                        num = str(i)
                        cv2.putText(result, num, (100+i*10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        event = i
                        flag = False
                if not flag :
                        outflag =True
                if not outflag:
                    event=-1
                                       
                if event == prev_event:
                    flag = True
                    continue
                elif event < 5 and event!= -1:
                    sound(event,midi_filename)
                elif event != -1:
                    sound(event-5,midi_filename)
                # elif event == 1:
                #     sound(event,midi_filename)
                # elif event == 2:
                #     sound(event,midi_filename)
                # elif event == 3:
                #     sound(event,midi_filename)
                # elif event == 4:
                #     sound(event,midi_filename)                 
                prev_event = event
                print("---")

           
    # 영역 표시 
    # cv2.rectangle(result, (80, 300),(180, 360),(0,0,255),2),  #도 
    # cv2.rectangle(result,(180, 300),(280, 360),(54,148,255),2)  #레
    # cv2.rectangle(result,(280, 300),(380, 360),(0,228,255),2)  #미
    # cv2.rectangle(result,(380, 300),(480, 360),(22,219,29),2)  #파
    # cv2.rectangle(result,(480, 300),(580, 360),(22,2,29),2)  #파

    for area in areas:
        cv2.rectangle(result, (area[0], area[1]),(area[2], area[3]), (0, 255, 0), 2)


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

